#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Roberto Godoy
Version: 1.0.0-BETA
Descriptions: Dump and Restore two MySQL or single .sql file.add()
Date: 15-12-2032
"""

import os
import subprocess
import logging
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
arquivo_dump = 'rds_sync_temp.sql'
logging.basicConfig(filename="sync-rds-p2h.log", level=logging.INFO)

rds_production = {
      'host': os.getenv('DBO_HOST'),
      'usuario': os.getenv('DBO_USERNAME'),
      'banco': os.getenv('DBO_DATABASE'),
      'senha': os.getenv('DBO_PASSWORD')
}

rds_homolog = {
      'host': os.getenv('DBD_HOST'),
      'usuario': os.getenv('DBD_USERNAME'),
      'banco': os.getenv('DBD_DATABASE'),
      'senha': os.getenv('DBD_PASSWORD')
}

def syncStart():
      if os.path.exists(arquivo_dump): os.remove(arquivo_dump)
      try:
            cmd = f"mysqldump -h {rds_production['host']} -u {rds_production['usuario']} -p{rds_production['senha']} --single-transaction  --set-gtid-purged=OFF --databases {rds_production['banco']} > {arquivo_dump}"
            logging.info(f" | {datetime.now()} | Dump do banco de dados PROD ({rds_production}), iniciado com sucesso.")
            subprocess.run(cmd, shell=True, check=True)
            logging.info(f" | {datetime.now()} | Dump do banco de dados PROD ({rds_production}),concluído com sucesso.")
            syncRestore()
      except subprocess.CalledProcessError as e:
            logging.info(f" | {datetime.now()} | Erro durante o dump: {e, rds_production['host']}")

def syncRestore():
      try:
            cmd = f"mysql -h {rds_homolog['host']} -u {rds_homolog['usuario']} -p{rds_homolog['senha']} {rds_homolog['banco']} < {arquivo_dump}"
            logging.info(f" | {datetime.now()} | Restore do banco de dados HOMOLG ({rds_homolog}), iniciado com sucesso.")
            subprocess.run(cmd, shell=True, check=True)
            logging.info(f" | {datetime.now()} | Restore do banco de dados HOMOLG ({rds_homolog}), concluído com sucesso.")
            if os.path.exists(arquivo_dump): os.remove(arquivo_dump)
      except subprocess.CalledProcessError as e:
            logging.info(f" | {datetime.now()} | Erro durante o restore: {e, rds_homolog['host']}")

if __name__ == '__main__':
      syncStart()