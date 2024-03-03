variable "bucket_name" {
  type        = string
  default     = "sure-thing"
  description = "bucket name"
}

variable "keep_n_deploys" {
  type        = number
  default     = 5
  description = "number of deploys to keep"
}
