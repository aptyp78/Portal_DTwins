-- ============================================
-- Portal_DTwins Database Schema v1.0
-- PostgreSQL + pgvector
-- Created: 2025-11-30
-- ============================================

-- Включаем расширение для векторного поиска
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- ENUM TYPES
-- ============================================

CREATE TYPE material_category AS ENUM (
    'RAW_SOURCES',
    'ANALYTICAL_NODES',
    'KNOWLEDGE_GRAPH',
    'SCHEMAS',
    'INDEXES',
    'DOCUMENTATION',
    'ARCHIVE',
    'GOLD'
);

CREATE TYPE material_status AS ENUM (
    'production',
    'immutable',
    'draft',
    'archived',
    'deprecated'
);

CREATE TYPE layer_type AS ENUM (
    'L1-Strategic',
    'L2-Operational',
    'L3-Technical'
);

CREATE TYPE edge_type AS ENUM (
    'derives_from',
    'references',
    'depends_on',
    'enables',
    'part_of',
    'influences',
    'funds',
    'regulates',
    'implements'
);

-- ============================================
-- CORE TABLES
-- ============================================

-- Основная таблица материалов
CREATE TABLE materials (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    material_id VARCHAR(50) UNIQUE NOT NULL,  -- e.g., NODE-CONTEXT, SRC-DOC-001
    filename VARCHAR(255) NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    category material_category NOT NULL,
    status material_status NOT NULL DEFAULT 'production',
    layer layer_type,
    file_path VARCHAR(500) NOT NULL,
    file_size_bytes BIGINT,
    file_hash VARCHAR(64),  -- SHA-256 для проверки целостности
    mime_type VARCHAR(100),

    -- Метаданные
    metadata JSONB DEFAULT '{}',
    tags VARCHAR(100)[] DEFAULT '{}',

    -- Версионность
    version VARCHAR(20) DEFAULT '1.0.0',
    version_date TIMESTAMP WITH TIME ZONE,

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    archived_at TIMESTAMP WITH TIME ZONE,

    -- Векторное представление для семантического поиска
    embedding vector(1536),  -- OpenAI ada-002 dimension

    -- Constraints
    CONSTRAINT valid_material_id CHECK (material_id ~ '^(SRC|NODE|GRAPH|SCHEMA|IDX|REG|DOC|GOLD)-[A-Z0-9-]+$')
);

-- Таблица первоисточников (расширение materials)
CREATE TABLE source_documents (
    id UUID PRIMARY KEY REFERENCES materials(id) ON DELETE CASCADE,
    document_number INTEGER,
    document_date DATE,
    author VARCHAR(255),
    organization VARCHAR(255),
    page_count INTEGER,
    has_attachments BOOLEAN DEFAULT FALSE,
    attachment_count INTEGER DEFAULT 0,
    original_format VARCHAR(20),  -- docx, pdf, xlsx
    extracted_text TEXT,
    extraction_date TIMESTAMP WITH TIME ZONE
);

-- Таблица аналитических узлов (расширение materials)
CREATE TABLE analytical_nodes (
    id UUID PRIMARY KEY REFERENCES materials(id) ON DELETE CASCADE,
    node_id VARCHAR(50) NOT NULL,  -- NODE-CONTEXT etc.
    layer layer_type NOT NULL,
    narrative_summary TEXT,
    key_concepts VARCHAR(255)[] DEFAULT '{}',
    backlinks_count INTEGER DEFAULT 0,
    outgoing_edges_count INTEGER DEFAULT 0,
    source_ids VARCHAR(50)[] DEFAULT '{}',  -- Ссылки на SRC-DOC-*

    -- Аналитические метрики
    importance_score DECIMAL(5,4) DEFAULT 0,  -- 0-1
    centrality_score DECIMAL(5,4) DEFAULT 0,

    CONSTRAINT valid_node_id CHECK (node_id ~ '^NODE-[A-Z]+$')
);

-- Таблица Knowledge Graph версий
CREATE TABLE knowledge_graphs (
    id UUID PRIMARY KEY REFERENCES materials(id) ON DELETE CASCADE,
    graph_version VARCHAR(10) NOT NULL,  -- v14
    nodes_count INTEGER NOT NULL,
    edges_count INTEGER NOT NULL,
    total_backlinks INTEGER DEFAULT 0,

    -- Граф в JSON для быстрого доступа
    nodes JSONB NOT NULL,
    edges JSONB NOT NULL,

    -- Метрики графа
    avg_degree DECIMAL(5,2),
    density DECIMAL(5,4),
    is_connected BOOLEAN,

    CONSTRAINT valid_version CHECK (graph_version ~ '^v[0-9]+$')
);

-- ============================================
-- RELATIONSHIP TABLES
-- ============================================

-- Связи между материалами (рёбра графа)
CREATE TABLE material_edges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_material_id UUID NOT NULL REFERENCES materials(id) ON DELETE CASCADE,
    target_material_id UUID NOT NULL REFERENCES materials(id) ON DELETE CASCADE,
    edge_type edge_type NOT NULL,
    weight DECIMAL(5,4) DEFAULT 1.0,
    description TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Уникальность связи
    CONSTRAINT unique_edge UNIQUE (source_material_id, target_material_id, edge_type)
);

-- Трассировка: Source -> Node
CREATE TABLE source_node_mapping (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID NOT NULL REFERENCES materials(id) ON DELETE CASCADE,
    node_id UUID NOT NULL REFERENCES materials(id) ON DELETE CASCADE,
    mapping_type VARCHAR(50) DEFAULT 'primary',  -- primary, secondary, reference
    confidence DECIMAL(3,2) DEFAULT 1.0,  -- 0-1
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT unique_source_node UNIQUE (source_id, node_id)
);

-- Backlinks (входящие ссылки)
CREATE TABLE backlinks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    target_node_id UUID NOT NULL REFERENCES materials(id) ON DELETE CASCADE,
    source_node_id UUID NOT NULL REFERENCES materials(id) ON DELETE CASCADE,
    reference_context TEXT,  -- Контекст упоминания
    reference_type VARCHAR(50),  -- concept, entity, relation
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT unique_backlink UNIQUE (target_node_id, source_node_id, reference_type)
);

-- ============================================
-- VERSION CONTROL
-- ============================================

-- История версий материалов
CREATE TABLE material_versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    material_id UUID NOT NULL REFERENCES materials(id) ON DELETE CASCADE,
    version VARCHAR(20) NOT NULL,
    version_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Snapshot данных на момент версии
    snapshot_path VARCHAR(500),  -- Путь к архиву версии
    snapshot_hash VARCHAR(64),
    changes_description TEXT,

    -- Кто создал версию
    created_by VARCHAR(100) DEFAULT 'system',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT unique_material_version UNIQUE (material_id, version)
);

-- ============================================
-- AGENT OPERATIONS
-- ============================================

-- Логирование операций агента
CREATE TABLE agent_operations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id VARCHAR(50) NOT NULL,  -- AGENT-KNOWLEDGE-GATE
    operation VARCHAR(100) NOT NULL,
    params JSONB DEFAULT '{}',

    -- Результат
    status VARCHAR(20) NOT NULL,  -- success, error, partial
    result JSONB,
    error_message TEXT,

    -- Материалы, затронутые операцией
    affected_materials UUID[] DEFAULT '{}',

    -- Timing
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_ms INTEGER,

    -- Context
    session_id UUID,
    request_context JSONB DEFAULT '{}'
);

-- Сессии агента
CREATE TABLE agent_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id VARCHAR(50) NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,

    -- Статистика сессии
    operations_count INTEGER DEFAULT 0,
    materials_accessed UUID[] DEFAULT '{}',

    -- Context
    session_context JSONB DEFAULT '{}'
);

-- ============================================
-- SEARCH & INDEXES
-- ============================================

-- Полнотекстовый поиск
CREATE TABLE search_index (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    material_id UUID NOT NULL REFERENCES materials(id) ON DELETE CASCADE,

    -- Текстовый контент для поиска
    content_text TEXT NOT NULL,
    content_tsvector tsvector,

    -- Метаданные для фильтрации
    category material_category,
    layer layer_type,
    tags VARCHAR(100)[] DEFAULT '{}',

    -- Векторное представление
    embedding vector(1536),

    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- INDEXES
-- ============================================

-- Materials indexes
CREATE INDEX idx_materials_material_id ON materials(material_id);
CREATE INDEX idx_materials_category ON materials(category);
CREATE INDEX idx_materials_status ON materials(status);
CREATE INDEX idx_materials_layer ON materials(layer);
CREATE INDEX idx_materials_tags ON materials USING GIN(tags);
CREATE INDEX idx_materials_metadata ON materials USING GIN(metadata);

-- Vector similarity search
CREATE INDEX idx_materials_embedding ON materials USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Edges indexes
CREATE INDEX idx_edges_source ON material_edges(source_material_id);
CREATE INDEX idx_edges_target ON material_edges(target_material_id);
CREATE INDEX idx_edges_type ON material_edges(edge_type);

-- Search indexes
CREATE INDEX idx_search_tsvector ON search_index USING GIN(content_tsvector);
CREATE INDEX idx_search_embedding ON search_index USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX idx_search_category ON search_index(category);

-- Agent operations indexes
CREATE INDEX idx_agent_ops_agent ON agent_operations(agent_id);
CREATE INDEX idx_agent_ops_operation ON agent_operations(operation);
CREATE INDEX idx_agent_ops_status ON agent_operations(status);
CREATE INDEX idx_agent_ops_started ON agent_operations(started_at);

-- ============================================
-- TRIGGERS
-- ============================================

-- Автообновление updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_materials_updated
    BEFORE UPDATE ON materials
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

-- Обновление tsvector при изменении контента
CREATE OR REPLACE FUNCTION update_search_tsvector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.content_tsvector = to_tsvector('russian', COALESCE(NEW.content_text, ''));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_search_tsvector
    BEFORE INSERT OR UPDATE OF content_text ON search_index
    FOR EACH ROW
    EXECUTE FUNCTION update_search_tsvector();

-- ============================================
-- VIEWS
-- ============================================

-- Обзор материалов с метриками
CREATE VIEW v_materials_overview AS
SELECT
    m.material_id,
    m.title,
    m.category,
    m.status,
    m.layer,
    m.file_size_bytes,
    m.version,
    m.created_at,
    m.updated_at,
    COALESCE(an.backlinks_count, 0) as backlinks_count,
    COALESCE(an.outgoing_edges_count, 0) as outgoing_edges_count,
    array_length(m.tags, 1) as tags_count
FROM materials m
LEFT JOIN analytical_nodes an ON m.id = an.id
WHERE m.status != 'archived';

-- Граф связей для визуализации
CREATE VIEW v_knowledge_graph AS
SELECT
    me.id as edge_id,
    sm.material_id as source_id,
    sm.title as source_title,
    tm.material_id as target_id,
    tm.title as target_title,
    me.edge_type,
    me.weight,
    sm.layer as source_layer,
    tm.layer as target_layer
FROM material_edges me
JOIN materials sm ON me.source_material_id = sm.id
JOIN materials tm ON me.target_material_id = tm.id
WHERE sm.status = 'production' AND tm.status = 'production';

-- Статистика по категориям
CREATE VIEW v_category_stats AS
SELECT
    category,
    COUNT(*) as total_count,
    COUNT(*) FILTER (WHERE status = 'production') as production_count,
    SUM(file_size_bytes) as total_size_bytes,
    AVG(file_size_bytes) as avg_size_bytes,
    MAX(updated_at) as last_updated
FROM materials
GROUP BY category;

-- ============================================
-- COMMENTS
-- ============================================

COMMENT ON TABLE materials IS 'Основная таблица всех материалов проекта Portal_DTwins';
COMMENT ON TABLE analytical_nodes IS 'Аналитические узлы Knowledge Graph (13 узлов)';
COMMENT ON TABLE source_documents IS 'Первоисточники: docx, pdf, xlsx (13 документов)';
COMMENT ON TABLE knowledge_graphs IS 'Версии Knowledge Graph';
COMMENT ON TABLE material_edges IS 'Рёбра графа связей между материалами';
COMMENT ON TABLE agent_operations IS 'Лог операций Knowledge Gate Agent';

COMMENT ON COLUMN materials.embedding IS 'Векторное представление для семантического поиска (OpenAI ada-002, 1536 dimensions)';
COMMENT ON COLUMN materials.material_id IS 'Уникальный ID материала по конвенции: SRC-*, NODE-*, GRAPH-*, SCHEMA-*, etc.';
