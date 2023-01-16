# Create Application Load balancer
# Edit DNS server
variable "service_name" {type = string}
variable "hosted_zone" {type = string}
variable "billing_tag" {type = string}
variable "s3_bucket" {type = string}

resource "aws_acm_certificate" "this" {
  domain_name       = "${var.service_name}.${var.hosted_zone}"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

# resource "aws_lb" "front_end" {
#   # ...
# }

# resource "aws_lb_target_group" "front_end" {
#   # ...
# }

# resource "aws_lb_listener" "front_end" {
#   load_balancer_arn = aws_lb.front_end.arn
#   port              = "443"
#   protocol          = "HTTPS"
#   ssl_policy        = "ELBSecurityPolicy-2016-08"
#   certificate_arn   = "arn:aws:iam::187416307283:server-certificate/test_cert_rab3wuqwgja25ct3n4jdj2tzu4"

#   default_action {
#     type             = "forward"
#     target_group_arn = aws_lb_target_group.front_end.arn
#   }
# }
resource "aws_vpc" "this" {
    cidr_block = "10.0.0.0/16"
}

variable "private_subnet" {
  type    = list
  default = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}
resource "aws_subnet" "this" {
  count                   = "${length(var.private_subnet)}"
  vpc_id                  = "${aws_vpc.this.id}"
  cidr_block              = "${var.private_subnet[count.index]}"
}

resource "aws_lb" "this" {
  # name               = "test-lb-tf"
  # internal           = false
  # load_balancer_type = "application"
  # security_groups    = [aws_security_group.lb_sg.id]
  subnets            = [for subnet in aws_subnet.this : subnet.id]

  # enable_deletion_protection = true

  access_logs {
    bucket  = var.s3_bucket
    prefix  = "lb"
    enabled = true
  }

  tags = {
    billing_tag = var.billing_tag
  }
}