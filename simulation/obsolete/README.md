

```bash

# You can bind any directory on your system to docker image by using -v flag:
# -v <your/directory>:<docker/directory>
# Convenient place inside docker image is
# /media/share
docker run -it --rm -v $(pwd):/media/share eicweb/jug_xl:nightly



# For X11 with new web root browser
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v $(pwd):/media/share --rm -it --user $(id -u) -p 9114:9114 eicweb/jug_xl:nightly

# Chain
docker run -it --rm -v $(pwd):/media/share eicweb/jug_xl:nightly
source /opt/detector/epic-nightly/setup.sh
cd /media/share/data/simulation
npsim --compactFile=$DETECTOR_PATH/ecce.xml --runType=run --enableG4GPS --macro disk_particle_gun.mac --outputFile=/media/share/data/disk_gun_electrons_0-15GeV_100ev.edm4hep.root 


# Spot particle gun
#100k e-
npsim --compactFile=$DETECTOR_PATH/ecce.xml --runType=run --enableG4GPS --macro spot_particle_gun.mac --outputFile=/media/share/data/spot_gun_electrons_0-12GeV_100000ev.edm4hep.root

# 1000 pi-
npsim --compactFile=$DETECTOR_PATH/ecce.xml --runType=run --enableG4GPS --macro spot_particle_gun.mac --outputFile=/media/share/data/spot_gun_pions_0-12GeV_1000ev.edm4hep.root
```

docker run -it --rm -v $(pwd):/media/share eicweb/jug_xl:nightly

electrons 100k events

https://drive.google.com/file/d/1aUBtJ9ki4Y0o_yPrHSO-vBu7YJK1NfbO/view?usp=sharing
https://doc-00-58-docs.googleusercontent.com/docs/securesc/sbhhbp9vpr3olhj6ui05acauhrerlo6k/qsql6censv3ptn1k3gbpnp3e992dvpko/1657828500000/10932611955762207609/10932611955762207609/1aUBtJ9ki4Y0o_yPrHSO-vBu7YJK1NfbO?e=download&ax=ACxEAsZS0qRXnCoGNMEpK2dsH2ZoCJLi8iOXaArXXAYEy93YJjC7ybEhDhSEMEEXxDcmxm6qdY7iRvxa7mNH6KxEjn2-_omjnOO2aBw_vkTZ57YlbF0xrY7zfNOHFyEQEiqPVxe25BFfmtzde1qR-hHNOdEQklxFGVGSOJUSyPSrhHX9kj3Whe-79Meweud0UgOUJBfK7GP0988C7_y9z56E2phKzCBcD_IRNKt0EI4ida5nvwFH_prE2uCtPHLYw-OCvZBX4FFwFmzT_wq9vDRKCqajV7JKCdlTpq6pGx7SpkuL4ubaUlba7rLeVnrl-k6QrpkKZbMHsG5yEP46_GvjGF37Rh_EN7TWIDnQo0Yvd1ehxhHlI7ERO6V39rQPtYGVaGhkeZujgWr_UhRyTga9yPq9RQ9Jab4hzscFdNoHx5ci4Td7oSJO14xFvhMec0qBOozN73M9lk2TDTBjS2AP3j0lD7jHDqngbO0PGJwTkw1K5U7mw88qBE7RNdXeE-XZ8iu5EScAnmIOSVCISAS5fFTWuNyM63XZdAxO4YYsyc3UeO4PgAvPqGsYlZXHZcHA6UedXC9Jy9oBx-wxVzM19UvNKYR12xTKilyhqCusiU0l254hck3MK0XiDD1OuKhgYjuePXKueatSzolngWUcyRLkWIKtMxI31Vs9rCtAo2RwunlAA-vrPmm2OuLMkLhedDwBmpIrecig82o-&uuid=2fb070dd-e3fd-4b5f-baba-bb9738e760c0&authuser=0&nonce=i4a51ppefto5a&user=10932611955762207609&hash=kj01taiumr9iltnukfd17idt701hu6us
https://drive.google.com/file/d/1aUBtJ9ki4Y0o_yPrHSO-vBu7YJK1NfbO/view?usp=sharing
```bash
wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=FILEID' -r -A 'uc*' -e robots=off -nd

wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1aUBtJ9ki4Y0o_yPrHSO-vBu7YJK1NfbO' -r -A 'uc*' -e robots=off -nd
```