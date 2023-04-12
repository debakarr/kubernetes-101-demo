# Kubernetes 101 Demo

## Opening KillerCoda Kubernetes Playground

![](https://i.imgur.com/VClirW8.jpg)
![](https://i.imgur.com/Q6k23Tx.jpg)
![](https://i.imgur.com/N4kXJfa.jpg)

---

## Configure KubeView

### Commands:
```console
git clone https://github.com/benc-uk/kubeview.git
helm install kubeview kubeview/charts/kubeview -f kubeview/charts/example-values.yaml 
k delete svc kubeview
k expose deploy kubeview --port 8000 --type NodePort
k get svc
```

### Output:
```console
controlplane $ git clone https://github.com/benc-uk/kubeview.git
Cloning into 'kubeview'...
remote: Enumerating objects: 1386, done.
remote: Counting objects: 100% (308/308), done.
remote: Compressing objects: 100% (160/160), done.
remote: Total 1386 (delta 160), reused 224 (delta 111), pack-reused 1078
Receiving objects: 100% (1386/1386), 5.17 MiB | 23.54 MiB/s, done.
Resolving deltas: 100% (757/757), done.


controlplane $ helm install kubeview kubeview/charts/kubeview -f kubeview/charts/example-values.yaml 
NAME: kubeview
LAST DEPLOYED: Tue Apr 11 04:22:45 2023
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
=====================================
==== KubeView has been deployed! ====
=====================================
  To get the external IP of your application, run the following:

  export SERVICE_IP=$(kubectl get svc --namespace default kubeview -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
  echo http://$SERVICE_IP

  NOTE: It may take a few minutes for the LoadBalancer IP to be available.
        You can watch the status of by running 'kubectl get --namespace default svc -w kubeview'
        
        
controlplane $ k delete svc kubeview
service "kubeview" deleted


controlplane $ k expose deploy kubeview --port 8000 --type NodePort
service/kubeview exposed


controlplane $ k get svc
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP          46d
kubeview     NodePort    10.98.130.239   <none>        8000:32727/TCP   2s
```

---

## Configure k8bits

### Commands:
```console
git clone https://github.com/learnk8s/k8bit.git
kubectl proxy --address='0.0.0.0' --port=8002 --accept-hosts='.*' --www=k8bit/ &
```

### Output:
```console
controlplane $ git clone https://github.com/learnk8s/k8bit.git
Cloning into 'k8bit'...
remote: Enumerating objects: 11, done.
remote: Counting objects: 100% (11/11), done.
remote: Compressing objects: 100% (9/9), done.
remote: Total 11 (delta 2), reused 11 (delta 2), pack-reused 0
Unpacking objects: 100% (11/11), 342.74 KiB | 11.42 MiB/s, done.


controlplane $ kubectl proxy --address='0.0.0.0' --port=8002 --accept-hosts='.*' --www=k8bit/ &
Starting to serve on [::]:8002
```

---

## Namespace

Create a namespace called 'demo' and set it as default

### Commands:
```console
k create ns demo
k config set-context --current --namespace=demo
```

### Output:
```console
controlplane $ k create ns demo
namespace/demo created


controlplane $ k config set-context --current --namespace=demo
Context "kubernetes-admin@kubernetes" modified.
```

---

## Pod

### Commands:
```console
k get pod
k run nginx --image nginx --port 80
k get pod -owide
```

### Output:
```console
controlplane $ k get pod
No resources found in demo namespace.


controlplane $ k run nginx --image nginx --port 80
pod/nginx created


controlplane $ k get pod -owide
NAME    READY   STATUS    RESTARTS   AGE   IP            NODE     NOMINATED NODE   READINESS GATES
nginx   1/1     Running   0          7s    192.168.1.3   node01   <none>           <none>


controlplane $ curl 192.168.1.3:80
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

---

## ReplicaSet

### Commands:
```console
cat > k8s-replicaset-nginx.yaml <<EOF
> apiVersion: apps/v1
> kind: ReplicaSet
> metadata:
>   labels:
>     run: nginx
>   name: nginx
> spec:
>   replicas: 3
>   selector:
>     matchLabels:
>       run: nginx
>   template:
>     metadata:
>       labels:
>         run: nginx
>       name: nginx
>     spec:
>       containers:
>         - image: nginx
>           name: nginx
>           ports:
>             - containerPort: 80
> EOF
k create -f k8s-replicaset-nginx.yaml 
k get rs
k get pod
```

### Output:
```console
controlplane $ cat > k8s-replicaset-nginx.yaml <<EOF
> apiVersion: apps/v1
> kind: ReplicaSet
> metadata:
>   labels:
>     run: nginx
>   name: nginx
> spec:
>   replicas: 3
>   selector:
>     matchLabels:
>       run: nginx
>   template:
>     metadata:
>       labels:
>         run: nginx
>       name: nginx
>     spec:
>       containers:
>         - image: nginx
>           name: nginx
>           ports:
>             - containerPort: 80
> EOF


controlplane $ k create -f k8s-replicaset-nginx.yaml 
replicaset.apps/nginx created


controlplane $ k get rs
NAME    DESIRED   CURRENT   READY   AGE
nginx   3         3         3       6s


controlplane $ k get pod
NAME          READY   STATUS    RESTARTS   AGE
nginx-9md6b   1/1     Running   0          11s
nginx-ttcvv   1/1     Running   0          11s
nginx-x5qtf   1/1     Running   0          11s
```

---

## Deployment

### Commands:
```console
k create deploy nginx --image nginx --port 80 --replicas 3
k get deploy
k get rs
k get pod -owide
curl 192.168.1.11:80
```

### Output:
```console
controlplane $ k create deploy nginx --image nginx --port 80 --replicas 3
deployment.apps/nginx created


controlplane $ k get deploy
NAME    READY   UP-TO-DATE   AVAILABLE   AGE
nginx   3/3     3            3           5s


controlplane $ k get rs
NAME               DESIRED   CURRENT   READY   AGE
nginx-7f456874f4   3         3         3       9s


controlplane $ k get pod
NAME                     READY   STATUS    RESTARTS   AGE
nginx-7f456874f4-cdvc9   1/1     Running   0          14s
nginx-7f456874f4-hbt6j   1/1     Running   0          14s
nginx-7f456874f4-mhc87   1/1     Running   0          14s


controlplane $ k get pod -owide
NAME                     READY   STATUS    RESTARTS   AGE   IP             NODE           NOMINATED NODE   READINESS GATES
nginx-7f456874f4-cdvc9   1/1     Running   0          26s   192.168.1.11   node01         <none>           <none>
nginx-7f456874f4-hbt6j   1/1     Running   0          26s   192.168.1.10   node01         <none>           <none>
nginx-7f456874f4-mhc87   1/1     Running   0          26s   192.168.0.11   controlplane   <none>           <none>


controlplane $ curl 192.168.1.11:80
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>


controlplane $ curl 192.168.0.11:80
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
controlplane $ 
```

---

## Deployment rolling update

### Commands:
```console
k create deploy nginx --image nginx:1.22.1 --port 80 --replicas 3
k get deploy
k get rs
k get pod
k describe deploy nginx
k set image deploy nginx nginx=nginx:1.23.4
k get deploy
k get rs
k get pod
k describe deploy nginx
```

### Output:
```console
controlplane $ k create deploy nginx --image nginx:1.22.1 --port 80 --replicas 3
deployment.apps/nginx created


controlplane $ k get deploy
NAME    READY   UP-TO-DATE   AVAILABLE   AGE
nginx   3/3     3            3           6s


controlplane $ k get rs
NAME               DESIRED   CURRENT   READY   AGE
nginx-579c9dfc44   3         3         3       9s


controlplane $ k get pod 
NAME                     READY   STATUS    RESTARTS   AGE
nginx-579c9dfc44-7cw8w   1/1     Running   0          14s
nginx-579c9dfc44-b896w   1/1     Running   0          14s
nginx-579c9dfc44-pnqx5   1/1     Running   0          14s


controlplane $ k describe deploy nginx
Name:                   nginx
Namespace:              demo
CreationTimestamp:      Wed, 12 Apr 2023 02:50:32 +0000
Labels:                 app=nginx
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=nginx
Replicas:               3 desired | 3 updated | 3 total | 3 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=nginx
  Containers:
   nginx:
    Image:        nginx:1.22.1
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   nginx-579c9dfc44 (3/3 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  21s   deployment-controller  Scaled up replica set nginx-579c9dfc44 to 3
  
  
controlplane $ k set image deploy nginx nginx=nginx:1.23.4
deployment.apps/nginx image updated


controlplane $ k get deploy
NAME    READY   UP-TO-DATE   AVAILABLE   AGE
nginx   3/3     3            3           43s


controlplane $ k get rs
NAME               DESIRED   CURRENT   READY   AGE
nginx-579c9dfc44   0         0         0       45s
nginx-7b8cbd4f76   3         3         3       6s


controlplane $ k get pod
NAME                     READY   STATUS    RESTARTS   AGE
nginx-7b8cbd4f76-44wvv   1/1     Running   0          13s
nginx-7b8cbd4f76-9qpxm   1/1     Running   0          12s
nginx-7b8cbd4f76-lgd8n   1/1     Running   0          10s


controlplane $ k describe deploy nginx
Name:                   nginx
Namespace:              demo
CreationTimestamp:      Wed, 12 Apr 2023 02:50:32 +0000
Labels:                 app=nginx
Annotations:            deployment.kubernetes.io/revision: 2
Selector:               app=nginx
Replicas:               3 desired | 3 updated | 3 total | 3 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=nginx
  Containers:
   nginx:
    Image:        nginx:1.23.4
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   nginx-7b8cbd4f76 (3/3 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  60s   deployment-controller  Scaled up replica set nginx-579c9dfc44 to 3
  Normal  ScalingReplicaSet  21s   deployment-controller  Scaled up replica set nginx-7b8cbd4f76 to 1
  Normal  ScalingReplicaSet  20s   deployment-controller  Scaled down replica set nginx-579c9dfc44 to 2 from 3
  Normal  ScalingReplicaSet  20s   deployment-controller  Scaled up replica set nginx-7b8cbd4f76 to 2 from 1
  Normal  ScalingReplicaSet  18s   deployment-controller  Scaled down replica set nginx-579c9dfc44 to 1 from 2
  Normal  ScalingReplicaSet  18s   deployment-controller  Scaled up replica set nginx-7b8cbd4f76 to 3 from 2
  Normal  ScalingReplicaSet  17s   deployment-controller  Scaled down replica set nginx-579c9dfc44 to 0 from 1
```

---

## Deployment rollback

### Commands:
```console
k create deploy nginx --image nginx:1.22.1 --port 80 --replicas 3
k set image deploy nginx nginx=nginx:1.23.4
k rollout history deploy nginx
k describe deploy nginx
k rollout undo deploy nginx --to-revision=1
k describe deploy nginx
```

### Output:
```console
controlplane $ k create deploy nginx --image nginx:1.22.1 --port 80 --replicas 3
deployment.apps/nginx created


controlplane $ k set image deploy nginx nginx=nginx:1.23.4
deployment.apps/nginx image updated


controlplane $ k rollout history deploy nginx
deployment.apps/nginx 
REVISION  CHANGE-CAUSE
1         <none>
2         <none>



controlplane $ k describe deploy nginx
Name:                   nginx
Namespace:              demo
CreationTimestamp:      Wed, 12 Apr 2023 02:57:17 +0000
Labels:                 app=nginx
Annotations:            deployment.kubernetes.io/revision: 2
Selector:               app=nginx
Replicas:               3 desired | 3 updated | 3 total | 3 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=nginx
  Containers:
   nginx:
    Image:        nginx:1.23.4
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   nginx-7b8cbd4f76 (3/3 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  21s   deployment-controller  Scaled up replica set nginx-579c9dfc44 to 3
  Normal  ScalingReplicaSet  15s   deployment-controller  Scaled up replica set nginx-7b8cbd4f76 to 1
  Normal  ScalingReplicaSet  14s   deployment-controller  Scaled down replica set nginx-579c9dfc44 to 2 from 3
  Normal  ScalingReplicaSet  14s   deployment-controller  Scaled up replica set nginx-7b8cbd4f76 to 2 from 1
  Normal  ScalingReplicaSet  12s   deployment-controller  Scaled down replica set nginx-579c9dfc44 to 1 from 2
  Normal  ScalingReplicaSet  12s   deployment-controller  Scaled up replica set nginx-7b8cbd4f76 to 3 from 2
  Normal  ScalingReplicaSet  11s   deployment-controller  Scaled down replica set nginx-579c9dfc44 to 0 from 1
  
  
controlplane $ k rollout undo deploy nginx --to-revision=1
deployment.apps/nginx rolled back


controlplane $ k describe deploy nginx
Name:                   nginx
Namespace:              demo
CreationTimestamp:      Wed, 12 Apr 2023 02:57:17 +0000
Labels:                 app=nginx
Annotations:            deployment.kubernetes.io/revision: 3
Selector:               app=nginx
Replicas:               3 desired | 3 updated | 4 total | 4 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=nginx
  Containers:
   nginx:
    Image:        nginx:1.22.1
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    ReplicaSetUpdated
OldReplicaSets:  <none>
NewReplicaSet:   nginx-579c9dfc44 (3/3 replicas created)
Events:
  Type    Reason             Age              From                   Message
  ----    ------             ----             ----                   -------
  Normal  ScalingReplicaSet  31s              deployment-controller  Scaled up replica set nginx-579c9dfc44 to 3
  Normal  ScalingReplicaSet  25s              deployment-controller  Scaled up replica set nginx-7b8cbd4f76 to 1
  Normal  ScalingReplicaSet  24s              deployment-controller  Scaled down replica set nginx-579c9dfc44 to 2 from 3
  Normal  ScalingReplicaSet  24s              deployment-controller  Scaled up replica set nginx-7b8cbd4f76 to 2 from 1
  Normal  ScalingReplicaSet  22s              deployment-controller  Scaled down replica set nginx-579c9dfc44 to 1 from 2
  Normal  ScalingReplicaSet  22s              deployment-controller  Scaled up replica set nginx-7b8cbd4f76 to 3 from 2
  Normal  ScalingReplicaSet  21s              deployment-controller  Scaled down replica set nginx-579c9dfc44 to 0 from 1
  Normal  ScalingReplicaSet  4s               deployment-controller  Scaled up replica set nginx-579c9dfc44 to 1 from 0
  Normal  ScalingReplicaSet  3s               deployment-controller  Scaled down replica set nginx-7b8cbd4f76 to 2 from 3
  Normal  ScalingReplicaSet  0s (x4 over 3s)  deployment-controller  (combined from similar events): Scaled down replica set nginx-7b8cbd4f76 to 0 from 1
```

---

## Services - ClusterIP

### Commands:
```console
k create deploy my-app --image=debakarr/simple-fastapi-app:1.0.0 --replicas=10 --port 80
k expose deploy my-app --port 80
k get svc
k run nginx --image nginx --port 80
k exec -it nginx -- sh
curl my-app:80
```

### Output:
```console
controlplane $ k create deploy my-app --image=debakarr/simple-fastapi-app:1.0.0 --replicas=10 --port 80
deployment.apps/my-app created


controlplane $ k expose deploy my-app --port 80
service/my-app exposed


controlplane $ k get svc
NAME     TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
my-app   ClusterIP   10.107.200.60   <none>        80/TCP    1s


controlplane $ k run nginx --image nginx --port 80
pod/nginx created


controlplane $ k get pod
NAME                      READY   STATUS              RESTARTS   AGE
my-app-5fb74f57dd-25bn5   1/1     Running             0          15s
my-app-5fb74f57dd-6jr7h   1/1     Running             0          16s
my-app-5fb74f57dd-75j7q   1/1     Running             0          15s
my-app-5fb74f57dd-g75km   1/1     Running             0          16s
my-app-5fb74f57dd-jfwf4   1/1     Running             0          15s
my-app-5fb74f57dd-mfq6p   1/1     Running             0          15s
my-app-5fb74f57dd-qh76r   1/1     Running             0          15s
my-app-5fb74f57dd-s6fxs   1/1     Running             0          16s
my-app-5fb74f57dd-vvzfm   1/1     Running             0          15s
my-app-5fb74f57dd-zgnvd   1/1     Running             0          15s
nginx                     1/1     Running             0          14s


controlplane $ k exec -it nginx -- sh
# curl my-app

    <html>
        <head>
            <title>Simple Application</title>
            <style>
                body {
                    background-color: #0072c9;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                div {
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <div>
                <h1>Hello, world!</h1>
                <h2>This is my-app-5fb74f57dd-zgnvd</h2>
            </div>
        </body>
    </html>
    # curl my-app

    <html>
        <head>
            <title>Simple Application</title>
            <style>
                body {
                    background-color: #0072c9;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                div {
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <div>
                <h1>Hello, world!</h1>
                <h2>This is my-app-5fb74f57dd-g75km</h2>
            </div>
        </body>
    </html>
    # exit
```

---

## Services - NodePort

### Commands:
```console
k create deploy my-app --image=debakarr/simple-fastapi-app:1.0.0 --replicas=10 --port 80
k expose deploy my-app --port 80 --type NodePort
k get svc
```

### Output:
```console
controlplane $ k create ns demo
namespace/demo created


controlplane $ k config set-context --current --namespace=demo
Context "kubernetes-admin@kubernetes" modified.


controlplane $ k create deploy my-app --image=debakarr/simple-fastapi-app:1.0.0 --replicas=10 --port 80
deployment.apps/my-app created


controlplane $ k expose deploy my-app --port 80 --type NodePort
service/my-app exposed


controlplane $ k get svc
NAME     TYPE       CLUSTER-IP    EXTERNAL-IP   PORT(S)        AGE
my-app   NodePort   10.108.4.15   <none>        80:32254/TCP   22s
```
