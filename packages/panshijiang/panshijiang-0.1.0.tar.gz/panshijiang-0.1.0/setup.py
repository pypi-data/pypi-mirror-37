from setuptools import setup, find_packages

setup(
  name="panshijiang",  # 项目代码所在目录
  version="0.1.0",
  keywords = ("pip", "pathtool","timetool", "magetool", "mage"),
  description="潘仕江测试包",
  long_description="潘仕江测试包",
  license="MIT Licence",

  url="https://github.com/fengmm521/pipProject",
  author="mage",
  author_email="mage@woodcol.com",

  packages=find_packages(),  # 这个参数是导入目录下的所有__init__.py包
  include_package_data=True,
  platforms="any",
  install_requires=[]  # 里边包含的是咱的pip项目引用到的第三方库
)