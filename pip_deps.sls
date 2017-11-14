python-pip:
  pkg.installed

pip-boto3:
  pip.installed:
    - name: boto3
    - reload_modules: True
    - require:
      - pkg: python-pip

pip-jmespath:
  pip.installed:
    - name: jmespath
    - reload_modules: True
    - require:
      - pkg: python-pip

pip-aws-decorators:
  pip.installed:
    - name: aws-decorators
    - reload_modules: True
    - require:
      - pkg: python-pip
