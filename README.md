# Autoclock RPC

### What is it good for?

The goal of the Autoclock RPC ansible playbook is to have you caught up on the Solana blockchain within 15 minutes, assuming you have a capable server and your SSH key ready. 

It formats/raids/mounts disks, sets up swap, ramdisk (optional), downloads from snapshot and restarts everything. 

It is currently configured for a Latitude.sh s3.large.x86 (see "Optimal Machine Settings" below), but we hope to adapt it more widely later on. 

For a more catch-all ansible playbook and in depth guide on RPC's refer to https://github.com/rpcpool/solana-rpc-ansible

### Optimal Machine Settings

- Our Latitude.sh s3.large.x86 server starts with the settings below, which we prefer because:

  - The initial state of the machine is cleaner than others that we have tried
  - Disks are named consistently (nvme01, nvme0n2)
  - Ubuntu installed (preferably ubuntu 20.04, 22.04) - this won't work with centos, etc. since they don't use aptitude by default
  - The login user being ubuntu helps (all the solana operations are done using the solana user that the ansible playbook creates)
  - Ubuntu is in the sudoer's list
  - Unmounted disks are clean - if your root is on one of partitions and you pass it as an argument, this could be disastrous

- All the above are satisfied by a fresh s3.large.x86 launch found here: https://www.latitude.sh/pricing
- Zen3 AMD Epyc’s such as the 7443p are considered some of the most performant nodes for keeping up with the tip of the chain at the moment, and support large amounts of RAM.

- Recommended RPC Specs
  - 24 cores or more (2.85GHz minimum)
  - 512 GB RAM if you want to use ramdisk/tmpfs and store the accounts db in RAM (we use 300 GB for ram disk). without tmpfs, the ram requirement can be significantly lower (~256 GB)
  - 3-4 TB (multiple disks is okay - i.e. 2x 1.9TB - because the ansible playbook stripes them together)

### Step 1: Deploy your machine

  - If you are using latitude.sh infrastructure, you should go with the s3.large.x86
  - Select OS: Choose between Ubuntu 20.04 or Ubuntu 22.04
  - Select your SSH Key: Leave it Blank if you want to connect to SSH using credentials, or select the SSH previously created through the UI
  - User Data: Leave it blank
  - Select No RAID (As we are building the RAID through the ansible playbook below already)
  - Hostname: No need to change

### Step 2: SSH into your machine

### Step 3: Start a screen session

```
screen -S sol
```

### Step 4: Install ansible

```
sudo apt-get install ansible -y
```

### Step 5: Clone the autoclock-rpc repository

```
git clone https://github.com/overclock-validator/autoclock-rpc.git
```

### Step 6: cd into the autoclock-rpc folder

```
cd autoclock-rpc
```

### Step 7: Run the ansible command

- this command can take between 10-20 minutes based on the specs of the machine
- it takes long because it does everything necessary to start the validator (format disks, checkout the solana repo, build it and download the latest snapshot, etc.)
- make sure that the solana_version is up to date (see below)
- check the values set in `defaults/main.yml` and update to the values you want

```
time ansible-playbook runner.yaml
```

#### ~ Parameters explained ~

- solana_version: the version of solana that we want to run. Check the Solana Tech discord’s mb-announcements channel for the recommended version.
- swap_mb: megabytes of swap. This can be set this to 50% of RAM or even lower. 100 GB is fine on a 512 GB RAM machine (variable value is in MB so 100000)
- raw_disk_list: the list of currently unmounted disks that will be wiped, raided, formatted with ext4 and then mounted to /mnt
- ramdisk_size: this is optional and only necessary if you want to use ramdisk for the validator - carves out a large portion of the RAM to store the accountsdb. On a 512 GB RAM instance, this can be set to 300 GB (variable value is in GB so 300)
- solana_installer: whether to install solana from the installer. If set to false it will build solana cli from the solana github

### Step 8: Once ansible finishes, switch to the solana user with:

```
sudo su - solana
```

### Step 9: Check the status

```
source ~/.profile
solana-validator --ledger /mnt/solana-ledger monitor
ledger monitor
Ledger location: /mnt/solana-ledger
⠉ Validator startup: SearchingForRpcService...
```

#### Initially the monitor should just show the below message which will last for a few minutes and is normal:

```
⠉ Validator startup: SearchingForRpcService...
```

#### After a while, the message at the terminal should change to something similar to this:

```
⠐ 00:08:26 | Processed Slot: 156831951 | Confirmed Slot: 156831951 | Finalized Slot: 156831917 | Full Snapshot Slot: 156813730 |
```

#### Check whether the RPC is caught up with the rest of the cluster with:

```
solana catchup --our-localhost
```

If you see the message above, then everything is working fine! Gratz. You have a new RPC server and you can visit the URL at http://xx.xx.xx.xx:8899/
