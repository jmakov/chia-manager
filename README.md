# Chia manager

## CLI reference
https://github.com/Chia-Network/chia-blockchain/wiki/CLI-Commands-Reference

## Remote UI access
`$export CHIA_ROOT=~/.chia/mainnet/`

https://github.com/Chia-Network/chia-blockchain/wiki/Connecting-the-UI-to-a-remote-daemon

## Disable external disks spinning down  
`$ crontab -e`

`*/5 * * * * /home/toaster/workspace/chia-manager/scripts/keep_hdds_spinning.sh /media/toaster`


# Requirements
## worker_starter
Expects to be writable: /var/log/chia-manager/workers