# module "alb" {
#   source = "github.com/lean-delivery/tf-module-aws-alb"

#   project     = "yelb"
#   environment = "dev"

#   vpc_id  = "vpc-eizox8ea"
#   subnets = ["subnet-sait0aiw", "subnet-op8phee4", "subnet-eego9xoo"]

#   acm_cert_domain = "*.project.example.com"
#   root_domain     = "example.com"

#   alb_logs_lifecycle_rule_enabled = true
#   alb_logs_expiration_days        = 5
# }
