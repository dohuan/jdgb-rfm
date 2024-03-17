export TF_IN_AUTOMATION = true

%-terraform-init:
	terraform init -backend-config=$*.hcl -input=false -reconfigure

%-terraform-plan:
	terraform plan -var-file=$*.tfvars -out=$*.tfplan -input=false -lock=false

%-terraform-plan-destroy:
	terraform plan -destroy -var-file=$*.tfvars -out=$*.tfplan -input=false -lock=false

%-terraform-apply:
	terraform apply -input=false -lock=false $*.tfplan

