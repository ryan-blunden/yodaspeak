terraform {
  required_providers {
    coder = {
      source = "coder/coder"
    }
    kubernetes = {
      source = "hashicorp/kubernetes"
    }
  }
}

provider "coder" {
}

variable "use_kubeconfig" {
  type        = bool
  description = <<-EOF
  Use host kubeconfig? (true/false)

  Set this to false if the Coder host is itself running as a Pod on the same
  Kubernetes cluster as you are deploying workspaces to.

  Set this to true if the Coder host is running outside the Kubernetes cluster
  for workspaces.  A valid "~/.kube/config" must be present on the Coder host.
  EOF
  default     = false
}

variable "namespace" {
  type        = string
  description = "The Kubernetes namespace to create workspaces in (must exist prior to creating workspaces). If the Coder host is itself running as a Pod on the same Kubernetes cluster as you are deploying workspaces to, set this to the same namespace."
}

data "coder_parameter" "cpu" {
  name         = "cpu"
  display_name = "CPU"
  description  = "The number of CPU cores"
  default      = "2"
  icon         = "/icon/memory.svg"
  mutable      = true
  option {
    name  = "2 Cores"
    value = "2"
  }
  option {
    name  = "4 Cores"
    value = "4"
  }
  option {
    name  = "6 Cores"
    value = "6"
  }
  option {
    name  = "8 Cores"
    value = "8"
  }
}

data "coder_parameter" "memory" {
  name         = "memory"
  display_name = "Memory"
  description  = "The amount of memory in GB"
  default      = "2"
  icon         = "/icon/memory.svg"
  mutable      = true
  option {
    name  = "2 GB"
    value = "2"
  }
  option {
    name  = "4 GB"
    value = "4"
  }
  option {
    name  = "6 GB"
    value = "6"
  }
  option {
    name  = "8 GB"
    value = "8"
  }
}

data "coder_parameter" "home_disk_size" {
  name         = "home_disk_size"
  display_name = "Home disk size"
  description  = "The size of the home disk in GB"
  default      = "10"
  type         = "number"
  icon         = "/emojis/1f4be.png"
  mutable      = false
  validation {
    min = 1
    max = 99999
  }
}

data "coder_parameter" "doppler_token" {
  name         = "doppler_token"
  display_name = "Doppler token"
  description  = "The Doppler auth token for accessing config and secrets"
  default      = ""
  type         = "string"
  icon         = "https://cdn.sanity.io/images/q3zajrd2/production/eb59a0d9476af5bf529c9af207071a5a45252628-400x400.png"
  mutable      = true
  order   = 10
}

# EnvBox config
variable "create_tun" {
  type        = bool
  sensitive   = true
  description = "Add a TUN device to the workspace."
  default     = false
}

variable "create_fuse" {
  type        = bool
  description = "Add a FUSE device to the workspace."
  sensitive   = true
  default     = true
}

provider "kubernetes" {
  # Authenticate via ~/.kube/config or a Coder-specific ServiceAccount, depending on admin preferences
  config_path = var.use_kubeconfig == true ? "~/.kube/config" : null
}

data "coder_workspace" "me" {}
data "coder_workspace_owner" "me" {}

resource "coder_agent" "main" {
  os             = "linux"
  arch           = "amd64"
  startup_script = <<-EOT
    set -e

    # If workspace first launch
    if [ ! -f ~/.init_done ]; then

      if [ ! -f ~/.bashrc ]; then
        printf "\n[info]: adding default user files and enabling shell history\n"
        cp -rT /etc/skel ~
        echo -e "\nHISTCONTROL=ignoredups:erasedups\nshopt -s histappend\nPROMPT_COMMAND='history -a'\n" >> ~/.bashrc
      fi

      if [ ! -f ~/.ssh/known_hosts ]; then
        printf "\n[info]: adding github.com to ~/.ssh/known_hosts\n"
        mkdir ~/.ssh
        ssh-keyscan github.com >> ~/.ssh/known_hosts
      fi

      REPO_PATH="$HOME/yodaspeak"
      REPO_URL="git@github.com:ryan-blunden/yodaspeak.git"

      if [ ! -d "$REPO_PATH" ]; then
        printf "\n[info]: cloning yodaspeak repository\n"
        git clone "$REPO_URL" "$REPO_PATH"

        printf "\n[info]: creating virtualenv\n"
        cd "$REPO_PATH"
        python3 -m venv .venv 
        . .venv/bin/activate

        printf "\n[info]: Installing dependencies\n"
        cd "$REPO_PATH"
        pip install -r requirements/local.txt
      fi

      touch ~/.init_done
    fi
  EOT

  # The following metadata blocks are optional. They are used to display
  # information about your workspace in the dashboard. You can remove them
  # if you don't want to display any information.
  # For basic resources, you can use the `coder stat` command.
  # If you need more control, you can write your own script.
  metadata {
    display_name = "CPU Usage"
    key          = "0_cpu_usage"
    script       = "coder stat cpu"
    interval     = 10
    timeout      = 1
  }

  metadata {
    display_name = "RAM Usage"
    key          = "1_ram_usage"
    script       = "coder stat mem"
    interval     = 10
    timeout      = 1
  }

  metadata {
    display_name = "Home Disk"
    key          = "3_home_disk"
    script       = "coder stat disk --path $${HOME}"
    interval     = 60
    timeout      = 1
  }

  metadata {
    display_name = "CPU Usage (Host)"
    key          = "4_cpu_usage_host"
    script       = "coder stat cpu --host"
    interval     = 10
    timeout      = 1
  }

  metadata {
    display_name = "Memory Usage (Host)"
    key          = "5_mem_usage_host"
    script       = "coder stat mem --host"
    interval     = 10
    timeout      = 1
  }

  metadata {
    display_name = "Load Average (Host)"
    key          = "6_load_host"
    # get load avg scaled by number of cores
    script   = <<EOT
      echo "`cat /proc/loadavg | awk '{ print $1 }'` `nproc`" | awk '{ printf "%0.2f", $1/$2 }'
    EOT
    interval = 60
    timeout  = 1
  }
}

resource "kubernetes_persistent_volume_claim" "home" {
  metadata {
    name      = "coder-${data.coder_workspace.me.id}-home"
    namespace = var.namespace
    labels = {
      "app.kubernetes.io/name"     = "coder-pvc"
      "app.kubernetes.io/instance" = "coder-pvc-${data.coder_workspace.me.id}"
      "app.kubernetes.io/part-of"  = "coder"
      //Coder-specific labels.
      "com.coder.resource"       = "true"
      "com.coder.workspace.id"   = data.coder_workspace.me.id
      "com.coder.workspace.name" = data.coder_workspace.me.name
      "com.coder.user.id"        = data.coder_workspace_owner.me.id
      "com.coder.user.username"  = data.coder_workspace_owner.me.name
    }
    annotations = {
      "com.coder.user.email" = data.coder_workspace_owner.me.email
    }
  }
  wait_until_bound = false
  spec {
    access_modes = ["ReadWriteOnce"]
    resources {
      requests = {
        storage = "${data.coder_parameter.home_disk_size.value}Gi"
      }
    }
  }
}

resource "kubernetes_deployment" "main" {
  count = data.coder_workspace.me.start_count
  depends_on = [
    kubernetes_persistent_volume_claim.home
  ]
  wait_for_rollout = false
  metadata {
    name      = "coder-${data.coder_workspace.me.id}"
    namespace = var.namespace
    labels = {
      "app.kubernetes.io/name"     = "coder-workspace"
      "app.kubernetes.io/instance" = "coder-workspace-${data.coder_workspace.me.id}"
      "app.kubernetes.io/part-of"  = "coder"
      "com.coder.resource"         = "true"
      "com.coder.workspace.id"     = data.coder_workspace.me.id
      "com.coder.workspace.name"   = data.coder_workspace.me.name
      "com.coder.user.id"          = data.coder_workspace_owner.me.id
      "com.coder.user.username"    = data.coder_workspace_owner.me.name
    }
    annotations = {
      "com.coder.user.email" = data.coder_workspace_owner.me.email
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        "app.kubernetes.io/name"     = "coder-workspace"
        "app.kubernetes.io/instance" = "coder-workspace-${data.coder_workspace.me.id}"
        "app.kubernetes.io/part-of"  = "coder"
        "com.coder.resource"         = "true"
        "com.coder.workspace.id"     = data.coder_workspace.me.id
        "com.coder.workspace.name"   = data.coder_workspace.me.name
        "com.coder.user.id"          = data.coder_workspace_owner.me.id
        "com.coder.user.username"    = data.coder_workspace_owner.me.name
      }
    }
    strategy {
      type = "Recreate"
    }

    template {
      metadata {
        labels = {
          "app.kubernetes.io/name"     = "coder-workspace"
          "app.kubernetes.io/instance" = "coder-workspace-${data.coder_workspace.me.id}"
          "app.kubernetes.io/part-of"  = "coder"
          "com.coder.resource"         = "true"
          "com.coder.workspace.id"     = data.coder_workspace.me.id
          "com.coder.workspace.name"   = data.coder_workspace.me.name
          "com.coder.user.id"          = data.coder_workspace_owner.me.id
          "com.coder.user.username"    = data.coder_workspace_owner.me.name
        }
      }
      spec {
        container {
          name              = "dev"
          image             = "ghcr.io/coder/envbox:0.6.2"
          image_pull_policy = "Always"
          command           = ["/envbox", "docker"]

          security_context {
            privileged = true
          }

          resources {
            requests = {
              "cpu"    = "250m"
              "memory" = "512Mi"
            }
            limits = {
              "cpu"    = "${data.coder_parameter.cpu.value}"
              "memory" = "${data.coder_parameter.memory.value}Gi"
            }
          }

          env {
            name  = "DOPPLER_TOKEN"
            value = data.coder_parameter.doppler_token.value
          }

          env {
            name  = "CODER_AGENT_TOKEN"
            value = coder_agent.main.token
          }

          env {
            name  = "CODER_AGENT_URL"
            value = data.coder_workspace.me.access_url
          }

          env {
            name  = "CODER_INNER_IMAGE"
            value = "index.docker.io/ryanblunden/coder-base:latest"
          }   

          env {
            name  = "CODER_INNER_USERNAME"
            value = "coder"
          }

          env {
            name  = "CODER_INNER_ENVS"
            value = "DOPPLER_TOKEN"
          }

          env {
            name  = "CODER_BOOTSTRAP_SCRIPT"
            value = coder_agent.main.init_script
          }

          env {
            name  = "CODER_MOUNTS"
            value = "/home/coder:/home/coder"
          }

          env {
            name  = "CODER_ADD_FUSE"
            value = var.create_fuse
          }

          env {
            name  = "CODER_INNER_HOSTNAME"
            value = data.coder_workspace.me.name
          }

          env {
            name  = "CODER_ADD_TUN"
            value = var.create_tun
          }

          env {
            name = "CODER_CPUS"
            value_from {
              resource_field_ref {
                resource = "limits.cpu"
              }
            }
          }

          env {
            name = "CODER_MEMORY"
            value_from {
              resource_field_ref {
                resource = "limits.memory"
              }
            }
          }

          volume_mount {
            mount_path = "/home/coder"
            name       = "home"
            read_only  = false
            sub_path   = "home"
          }

          volume_mount {
            mount_path = "/var/lib/coder/docker"
            name       = "home"
            sub_path   = "cache/docker"
          }

          volume_mount {
            mount_path = "/var/lib/coder/containers"
            name       = "home"
            sub_path   = "cache/containers"
          }

          volume_mount {
            mount_path = "/var/lib/sysbox"
            name       = "sysbox"
          }

          volume_mount {
            mount_path = "/var/lib/containers"
            name       = "home"
            sub_path   = "envbox/containers"
          }

          volume_mount {
            mount_path = "/var/lib/docker"
            name       = "home"
            sub_path   = "envbox/docker"
          }

          volume_mount {
            mount_path = "/usr/src"
            name       = "usr-src"
          }

          volume_mount {
            mount_path = "/lib/modules"
            name       = "lib-modules"
          }
        }

        volume {
          name = "home"
          persistent_volume_claim {
            claim_name = kubernetes_persistent_volume_claim.home.metadata.0.name
            read_only  = false
          }
        }

        volume {
          name = "sysbox"
          empty_dir {}
        }

        volume {
          name = "usr-src"
          host_path {
            path = "/usr/src"
            type = ""
          }
        }

        volume {
          name = "lib-modules"
          host_path {
            path = "/lib/modules"
            type = ""
          }
        }

        affinity {
          // This affinity attempts to spread out all workspace pods evenly across
          // nodes.
          pod_anti_affinity {
            preferred_during_scheduling_ignored_during_execution {
              weight = 1
              pod_affinity_term {
                topology_key = "kubernetes.io/hostname"
                label_selector {
                  match_expressions {
                    key      = "app.kubernetes.io/name"
                    operator = "In"
                    values   = ["coder-workspace"]
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}

module "vscode-web" {
  source         = "registry.coder.com/modules/vscode-web/coder"
  version        = "1.0.22"
  agent_id       = coder_agent.main.id
  extensions     = ["github.copilot", "ms-python.python", "ms-azuretools.vscode-docker"]
  folder         = "/home/coder/yodaspeak"
  accept_license = true
}

module "dotfiles" {
  count                 = data.coder_workspace.me.start_count
  source                = "registry.coder.com/modules/dotfiles/coder"
  version               = "1.0.18"
  agent_id              = coder_agent.main.id
  coder_parameter_order = 20
}
