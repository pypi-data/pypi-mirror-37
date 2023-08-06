apiVersion: v1
kind: ConfigMap
metadata:
  name: aws-auth
  namespace: kube-system
data:
  mapRoles: |
  {{#node_roles}}
    - rolearn: {{arn}}
      username: {{=<% %>=}}system:node:{{EC2PrivateDNSName}}<%={{ }}=%>
      groups:
        - system:bootstrappers
        - system:nodes
  {{/node_roles}}
  {{#cluster_access_role}}
    - rolearn: {{arn}}
      username: {{name}}
      groups:
        - system:masters
  {{/cluster_access_role}}
