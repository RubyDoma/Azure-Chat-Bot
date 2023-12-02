
variable "subscription_id" {
  default = "f4b1e8d1-13bc-4b3a-aa0a-4c6f6459d9fc"

}

variable "tenantid" {
  default = "a8bc5e81-0953-44c1-9c13-4c8778633a76"

}

variable "clientsecret" {
  sensitive = true
}

variable "clientid" {
  sensitive = true
}


variable "app_id" {
  default = "605fa8e5-69e7-4511-98b2-ec7e22f52789"
}


variable "resourceGroupName" {
  default     = "AtlassianRG"
  description = "The name of the Resource Group"
}


variable "search_service" {
  default     = ""
  description = "The search service plan to use.  If none is passed it will create one"
}

variable "search_sku" {
  default     = "standard"
  description = "The sku to use for the azure search service"
}
