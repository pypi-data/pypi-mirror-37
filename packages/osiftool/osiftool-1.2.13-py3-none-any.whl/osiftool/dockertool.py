import docker


##########################################################################################

def fn_build() :
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    image = client.images.build(dockerfile="Dockerfile.rpi", tag="osif/iotweek-demo-button:rpi", path=".")
    print(image)

