apiVersion: batch/v1
kind: Job
metadata:
  name: {{job_name}}
spec:
  template:
    spec:
      containers:
      - name: orchestrate
        image: {{image_name}}
        env:
          - name: POD_NAME
            valueFrom:
              fieldRef:
                fieldPath: metadata.name
          {{#environment_variables}}
          - name: {{name}}
            value: "{{value}}"
          {{/environment_variables}}
        {{#resources}}
        resources:
          limits:
            nvidia.com/gpu: {{gpu_count}}
        {{/resources}}
      dnsPolicy: "None"
      dnsConfig:
        nameservers:
          - 8.8.8.8
          - 8.8.4.4
      restartPolicy: Never
  backoffLimit: 4
  parallelism: {{parallel_bandwidth}}
