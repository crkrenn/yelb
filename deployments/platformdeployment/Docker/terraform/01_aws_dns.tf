# aws route53 list-hosted-zones | grep -e Id -e Name
# terraform import aws_route53_zone.root <ID>

resource "aws_route53_zone" "root" {
    name = var.aws_root_domain
}

resource "aws_route53_zone" "dev" {
  name = "dev.${var.aws_root_domain}"
}

resource "aws_route53_record" "dev-ns" {
  zone_id = aws_route53_zone.root.zone_id
  name    = "dev.${var.aws_root_domain}"
  type    = "NS"
  ttl     = "30"
  records = aws_route53_zone.dev.name_servers
}

output "aws_route53_zone_dev" {
  value = aws_route53_zone.dev
}
