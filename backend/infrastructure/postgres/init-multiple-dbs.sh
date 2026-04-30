#!/bin/bash
# ==============================================================================
#  init-multiple-dbs.sh
#  Tạo nhiều PostgreSQL databases từ biến môi trường POSTGRES_MULTIPLE_DATABASES
#
#  CÁCH HOẠT ĐỘNG:
#  → Docker PostgreSQL image sẽ TỰ ĐỘNG chạy tất cả *.sh files trong thư mục
#    /docker-entrypoint-initdb.d/ KHI container khởi tạo lần đầu tiên
#  → Script này đọc biến POSTGRES_MULTIPLE_DATABASES (vd: "users_db,orders_db")
#    và tạo từng database một
#
#  LƯU Ý: Script này chỉ chạy khi data volume TRỐNG (lần đầu tiên)
#  Nếu volume đã có data, script này bị bỏ qua (idempotent behavior)
# ==============================================================================

set -e   # exit ngay nếu có lỗi
set -u   # lỗi nếu dùng biến chưa được set

# Hàm tạo 1 database với user có full permissions
create_database() {
    local database=$1
    echo "  → Creating database: '$database'"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
        CREATE DATABASE ${database};
        GRANT ALL PRIVILEGES ON DATABASE ${database} TO ${POSTGRES_USER};
EOSQL
    echo "  ✓ Database '${database}' created successfully"
}

# Main logic
if [ -n "${POSTGRES_MULTIPLE_DATABASES:-}" ]; then
    echo ""
    echo "================================================================"
    echo " PostgreSQL: Initializing multiple databases"
    echo " Databases to create: $POSTGRES_MULTIPLE_DATABASES"
    echo "================================================================"

    # Tách chuỗi bằng dấu phẩy, loop qua từng DB name
    IFS=',' read -ra DATABASES <<< "$POSTGRES_MULTIPLE_DATABASES"
    for db in "${DATABASES[@]}"; do
        # trim whitespace
        db=$(echo "$db" | xargs)
        create_database "$db"
    done

    echo ""
    echo "================================================================"
    echo " All databases initialized successfully!"
    echo "================================================================"
    echo ""
else
    echo "POSTGRES_MULTIPLE_DATABASES not set, skipping multi-db init"
fi
