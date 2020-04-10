#!/usr/bin/env bash

DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit ; pwd -P )
DEP=0

# Checking depenencies
mysqldump --version > /dev/null
if [ $(echo $?) -ne 0 ]; then
  >&2 echo "ERROR: mysqldump is missing"
  DEP=$((DEP + 1))
fi

wget --version > /dev/null
if [ $(echo $?) -ne 0 ]; then
  >&2 echo "ERROR: wget is missing"
  DEP=$((DEP + 1))
fi

unzip --help > /dev/null
if [ $(echo $?) -ne 0 ]; then
  >&2 echo "ERROR: unzip is missing"
  DEP=$((DEP + 1))
fi

if [ ${DEP} -ne 0 ]; then
  >&2 echo "ERROR: ${DEP} dependencies are missing"
  exit 1
fi

# Dumping tpcc mysql database
echo "INFO: Dumping tpcc from relational.fit.cvut.cz"
mysqldump -h relational.fit.cvut.cz -u guest -prelational tpcc --skip-extended-insert --compact > ${DIR}/tpcc.sql 2> /dev/null

# Downloading mysql2sqlite
echo "INFO: Downloading mysql2sqlite"
wget https://github.com/dumblob/mysql2sqlite/archive/master.zip -O ${DIR}/mysql2sqlite-master.zip &> /dev/null
unzip ${DIR}/mysql2sqlite-master.zip -d ${DIR}/ &> /dev/null

# Converting it to sqlite3 format
echo "INFO: Importing database to sqlite3"
TMP_FILE="${DIR}/.tmp"
rm -f ${DIR}/tpcc-xl.db \
    ${DIR}/tpcc-lg.db \
    ${DIR}/tpcc-md.db \
    ${DIR}/tpcc-sm.db \
    ${DIR}/tpcc-xs.db
    
${DIR}/mysql2sqlite-master/mysql2sqlite ${DIR}/tpcc.sql > ${TMP_FILE}
cat ${TMP_FILE} | ${DIR}/sqlite3 ${DIR}/tpcc-xl.db
cat ${TMP_FILE} | grep -v -E "INSERT INTO \`C_Customer\`" | grep -v -E "INSERT INTO \`C_District\`" | grep -v -E "INSERT INTO \`C_History\`" | grep -v -E "INSERT INTO \`C_New_Order\`" | grep -v -E "INSERT INTO \`C_Order_Line\`" | grep -v -E "INSERT INTO \`C_Stock\`" | grep -v -E "INSERT INTO \`C_Warehouse\`" | ${DIR}/sqlite3 ${DIR}/tpcc-lg.db
cat ${TMP_FILE} | grep -v -E "INSERT INTO \`C_Customer\`" | grep -v -E "INSERT INTO \`C_District\`" | grep -v -E "INSERT INTO \`C_History\`" | grep -v -E "INSERT INTO \`C_Item\`" | grep -v -E "INSERT INTO \`C_New_Order\`" | grep -v -E "INSERT INTO \`C_Order_Line\`" | grep -v -E "INSERT INTO \`C_Stock\`" | grep -v -E "INSERT INTO \`C_Warehouse\`" | ${DIR}/sqlite3 ${DIR}/tpcc-md.db
cat ${TMP_FILE} | grep -v -E "INSERT INTO \`C_Customer\`" | grep -v -E "INSERT INTO \`C_District\`" | grep -v -E "INSERT INTO \`C_History\`" | grep -v -E "INSERT INTO \`C_Item\`" | grep -v -E "INSERT INTO \`C_Order\`" | grep -v -E "INSERT INTO \`C_Order_Line\`" | grep -v -E "INSERT INTO \`C_Stock\`" | grep -v -E "INSERT INTO \`C_Warehouse\`" | ${DIR}/sqlite3 ${DIR}/tpcc-sm.db
cat ${TMP_FILE} | grep -v -E "INSERT INTO \`C_Customer\`" | grep -v -E "INSERT INTO \`C_District\`" | grep -v -E "INSERT INTO \`C_History\`" | grep -v -E "INSERT INTO \`C_Item\`" | grep -v -E "INSERT INTO \`C_New_Order\`" | grep -v -E "INSERT INTO \`C_Order\`" | grep -v -E "INSERT INTO \`C_Order_Line\`" | grep -v -E "INSERT INTO \`C_Stock\`" | ${DIR}/sqlite3 ${DIR}/tpcc-xs.db


# Removing dump and utils
echo "INFO: Cleaning temporary files"
rm -rf ${DIR}/tpcc.sql ${DIR}/mysql2sqlite-master ${DIR}/mysql2sqlite-master.zip ${TMP_FILE}

echo "Done"
