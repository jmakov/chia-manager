# Chia manager

## CLI reference
https://github.com/Chia-Network/chia-blockchain/wiki/CLI-Commands-Reference

## Remote UI access
`$export CHIA_ROOT=~/.chia/mainnet/`

https://github.com/Chia-Network/chia-blockchain/wiki/Connecting-the-UI-to-a-remote-daemon

## Disable external disks spinning down  
`$ crontab -e`

`*/5 * * * * /home/toaster/workspace/chia-manager/scripts/keep_hdds_spinning.sh /media/toaster`

## Disk optimizations
Disable reserved space:

`$sudo tune2fs -m0 /dev/DEVICE`

### Filesystem optimizations:
/etc/fstab:

#### SSD
`ext4 defaults,noiversion,auto_da_alloc,acl,user_xattr,noatime,nodiratime,nobarrier,discard,errors=remount-ro,commit=20,inode_readahead_blks=64,delalloc 0 1`

#### HDD
`ext4 defaults,noiversion,auto_da_alloc,acl,user_xattr,noatime,nodiratime,nobarrier,errors=remount-ro,commit=20,inode_readahead_blks=64,delalloc 0 1`

# Requirements
## worker_starter
Expects to be writable: /var/log/chia-manager/workers