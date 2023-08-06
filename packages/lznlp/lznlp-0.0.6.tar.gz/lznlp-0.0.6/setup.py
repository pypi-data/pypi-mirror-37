# -*- coding: utf-8 -*-
import setuptools

with open("README.md", encoding="utf8") as f:
    long_description = f.read()

setuptools.setup(name="lznlp",
                 version="0.0.6", 
                 author="liangzhi",
                 author_email="service@quant-chi.com",
                 description="LiangZhiNLP API wrapper",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="http://192.168.1.26:8099/liangzhi.ai/lznlp-platform/tree/master/scripts/lznlp.sdk",
                 packages=setuptools.find_packages(),
                 license="MIT",
                 classifiers=[
                     'Development Status :: 5 - Production/Stable',
                     'Intended Audience :: Developers',
                     'Operating System :: OS Independent',
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     'Topic :: Software Development :: Libraries :: Python Modules',
                     'Topic :: Software Development :: Testing',
                 ],
                 install_requires=[
                     "requests>=2.0.0",
                     "nose",
                     "fasttext",
                     "xgboost",
                     "pika"
                 ],
                 include_package_data=True,
                 zip_safe=False,
                 )
