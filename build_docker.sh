clear
NV="v1.6.1"

# =============================== build menjadi image docker =============================== #
docker build -t services-test:$NV .
docker image save -o services-test-$NV.tar services-test:$NV
# ssh surya@10.7.1.116 -p 24017 "cp ~/CombustionOpt/zipped/services-combustion-pct2-$OV.tar ~/CombustionOpt/zipped/services-combustion-pct2-$NV.tar"
# rsync -Pavre "ssh -p 24017" ../services-combustion-pct2-$NV.tar surya@10.7.1.116:~/CombustionOpt/zipped/.
# rsync -Pavre "ssh -p 24017" run_service_tar.sh surya@10.7.1.116:~/CombustionOpt/zipped/.
# ssh surya@10.7.1.116 -p 24017 'cd CombustionOpt/zipped/; ./run_service_tar.sh'

# =============================== gunakan command berikut (tanpa tanda "#") untuk pasang docker image ke container ================================== #
# docker stop services-test
# docker rm services-test
# docker image rm  services-test:$NV
# docker image load -i services-test-$NV.tar
# docker run -itd --name services-test --restart unless-stopped --memory="300M" -p 0.0.0.0:8083:8083 services-test:$NV
