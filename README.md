# Chia manager


## Disable external disks spinning down  
`$ crontab -e`

`*/5 * * * * /home/toaster/workspace/chia-manager/scripts/keep_external_hdds_running.sh
`