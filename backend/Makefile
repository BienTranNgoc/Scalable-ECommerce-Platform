# ==============================================================================
#  Makefile — Developer Shortcuts
#
#  Tại sao dùng Makefile?
#  → Thay vì nhớ lệnh dài: docker compose -f docker-compose.yml up -d postgres mongodb redis
#  → Chỉ cần: make up-db
#
#  DÙNG NHƯ THẾ NÀO:
#    make help     — xem tất cả commands
#    make setup    — setup lần đầu
#    make up       — start everything
#    make down     — stop everything
# ==============================================================================

.PHONY: help setup up down restart logs ps clean \
        up-db up-kafka up-search up-gateway up-discovery up-monitoring \
        down-db migrate shell-postgres shell-redis kafka-topics

# Colors
GREEN  := \033[0;32m
YELLOW := \033[1;33m
CYAN   := \033[0;36m
RESET  := \033[0m

# ==============================================================================
# HELP
# ==============================================================================
help: ## Hiển thị tất cả available commands
	@echo ""
	@echo "$(CYAN)╔══════════════════════════════════════════════╗$(RESET)"
	@echo "$(CYAN)║     E-Commerce Platform — Dev Commands       ║$(RESET)"
	@echo "$(CYAN)╚══════════════════════════════════════════════╝$(RESET)"
	@echo ""
	@echo "$(YELLOW)SETUP:$(RESET)"
	@grep -E '^(setup|env):.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)LIFECYCLE:$(RESET)"
	@grep -E '^(up|down|restart|logs|ps|clean):.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)START INDIVIDUAL BLOCKS:$(RESET)"
	@grep -E '^up-.*:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)DATABASE UTILS:$(RESET)"
	@grep -E '^(migrate|shell-|kafka-):.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""

# ==============================================================================
# SETUP
# ==============================================================================
setup: ## Khởi tạo project lần đầu (tạo .env file)
	@echo "$(CYAN)Setting up E-Commerce Platform...$(RESET)"
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "$(GREEN)✓ .env file created from .env.example$(RESET)"; \
		echo "$(YELLOW)→ Please edit .env and fill in your values$(RESET)"; \
	else \
		echo "$(YELLOW)→ .env already exists, skipping$(RESET)"; \
	fi
	@echo ""
	@echo "$(GREEN)Next steps:$(RESET)"
	@echo "  1. Edit .env with your configuration"
	@echo "  2. Run: make up"
	@echo "  3. Run: make ps (to check service status)"
	@echo ""

env: ## Kiểm tra .env file có tồn tại không
	@[ -f .env ] && echo "$(GREEN)✓ .env exists$(RESET)" || echo "$(YELLOW)⚠ .env not found — run: make setup$(RESET)"

# ==============================================================================
# LIFECYCLE COMMANDS
# ==============================================================================
up: env ## Start tất cả infrastructure services
	@echo "$(CYAN)Starting all services...$(RESET)"
	docker compose up -d
	@echo ""
	@echo "$(GREEN)Services started! Access points:$(RESET)"
	@echo "  API Gateway (Kong)     : http://localhost:8000"
	@echo "  Kong Admin UI          : http://localhost:8002"
	@echo "  Consul UI              : http://localhost:8500"
	@echo "  Kafka UI               : http://localhost:8080"
	@echo "  OpenSearch Dashboards  : http://localhost:5601"
	@echo "  Grafana                : http://localhost:3000  (admin/see .env)"
	@echo "  Prometheus             : http://localhost:9090"
	@echo "  Adminer (DB GUI)       : http://localhost:8090"
	@echo "  Redis Commander        : http://localhost:8091"
	@echo ""

down: ## Stop tất cả services (giữ nguyên volumes)
	@echo "$(YELLOW)Stopping all services...$(RESET)"
	docker compose down

restart: ## Restart tất cả services
	docker compose restart

logs: ## Xem logs của tất cả services (Ctrl+C để thoát)
	docker compose logs -f

ps: ## Liệt kê trạng thái tất cả containers
	docker compose ps

clean: ## ⚠️  XÓA TẤT CẢ containers + volumes (mất data!)
	@echo "$(YELLOW)⚠️  WARNING: This will delete ALL data in volumes!$(RESET)"
	@read -p "Are you sure? (yes/no): " confirm && [ "$$confirm" = "yes" ] || exit 1
	docker compose down -v --remove-orphans
	@echo "$(GREEN)✓ All containers and volumes removed$(RESET)"

# ==============================================================================
# START INDIVIDUAL SERVICE BLOCKS
# ==============================================================================
up-db: env ## Start chỉ databases (Postgres, MongoDB, Redis)
	docker compose up -d postgres mongodb redis
	@echo "$(GREEN)✓ Databases started$(RESET)"

up-kafka: env ## Start Kafka stack (Zookeeper + Kafka + Kafka UI)
	docker compose up -d zookeeper kafka kafka-ui

up-search: env ## Start OpenSearch + Dashboards
	docker compose up -d opensearch opensearch-dashboards

up-gateway: env ## Start Kong API Gateway
	docker compose up -d kong-migration kong

up-discovery: env ## Start Consul Service Discovery
	docker compose up -d consul

up-monitoring: env ## Start Prometheus + Grafana + Logstash
	docker compose up -d prometheus grafana logstash

# ==============================================================================
# DATABASE UTILITIES
# ==============================================================================
shell-postgres: ## Mở psql shell trong Postgres container
	docker compose exec postgres psql -U $${POSTGRES_USER} -d postgres

shell-redis: ## Mở redis-cli trong Redis container
	docker compose exec redis redis-cli -a $${REDIS_PASSWORD}

kafka-topics: ## Liệt kê tất cả Kafka topics
	docker compose exec kafka kafka-topics --bootstrap-server localhost:9092 --list

kafka-create-topics: ## Tạo các Kafka topics cho dự án
	@echo "Creating Kafka topics..."
	docker compose exec kafka kafka-topics --bootstrap-server localhost:9092 --create \
		--topic order.created --partitions 3 --replication-factor 1 --if-not-exists
	docker compose exec kafka kafka-topics --bootstrap-server localhost:9092 --create \
		--topic payment.completed --partitions 3 --replication-factor 1 --if-not-exists
	docker compose exec kafka kafka-topics --bootstrap-server localhost:9092 --create \
		--topic payment.failed --partitions 3 --replication-factor 1 --if-not-exists
	docker compose exec kafka kafka-topics --bootstrap-server localhost:9092 --create \
		--topic user.registered --partitions 3 --replication-factor 1 --if-not-exists
	docker compose exec kafka kafka-topics --bootstrap-server localhost:9092 --create \
		--topic notification.email --partitions 3 --replication-factor 1 --if-not-exists
	@echo "$(GREEN)✓ All Kafka topics created$(RESET)"
	@make kafka-topics

# Health check tất cả services
health: ## Kiểm tra health status của tất cả services
	@echo "$(CYAN)Checking service health...$(RESET)"
	@docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
