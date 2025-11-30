-- ============================================
-- Portal_DTwins Initial Seed Data
-- Загрузка материалов из Gold JSON
-- Created: 2025-11-30
-- ============================================

-- ============================================
-- RAW SOURCES (13 документов)
-- ============================================

INSERT INTO materials (material_id, filename, title, category, status, file_path, file_size_bytes, mime_type, metadata, tags)
VALUES
    ('SRC-DOC-001', '1_2025_11_Док_1_Банк_ПСБ.docx', 'Банк ПСБ — Логика акционера', 'RAW_SOURCES', 'immutable',
     'SOURCE_DOCUMENTS/1_2025_11_Док_1_Банк_ПСБ.docx', 152453,
     'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
     '{"document_number": 1, "document_date": "2025-11", "topic": "shareholder_logic"}',
     ARRAY['ПСБ', 'акционер', 'банк']),

    ('SRC-DOC-002', '2_2025_11_Док_2_Финансовая_Архитектура.docx', 'Финансовая архитектура', 'RAW_SOURCES', 'immutable',
     'SOURCE_DOCUMENTS/2_2025_11_Док_2_Финансовая_Архитектура.docx', 96857,
     'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
     '{"document_number": 2, "document_date": "2025-11", "topic": "financial_architecture"}',
     ARRAY['финансы', 'архитектура', 'инвестиции']),

    ('SRC-DOC-003', '3_2025_11_Док_3_Экосистема.docx', 'Экосистема ПСБ × СПбПУ', 'RAW_SOURCES', 'immutable',
     'SOURCE_DOCUMENTS/3_2025_11_Док_3_Экосистема.docx', 110426,
     'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
     '{"document_number": 3, "document_date": "2025-11", "topic": "ecosystem"}',
     ARRAY['экосистема', 'инфраструктура', 'СПбПУ']),

    ('SRC-DOC-004', '4_2025_11_Док_4_Контекст.docx', 'Общий контекст Замысла', 'RAW_SOURCES', 'immutable',
     'SOURCE_DOCUMENTS/4_2025_11_Док_4_Контекст.docx', 56820,
     'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
     '{"document_number": 4, "document_date": "2025-11", "topic": "context", "has_attachments": true, "attachment_count": 5}',
     ARRAY['контекст', 'замысел', 'стратегия']),

    ('SRC-DOC-005', '5_2025_11_Док_5_Глобальный.docx', 'Глобальный тренд — Платформа', 'RAW_SOURCES', 'immutable',
     'SOURCE_DOCUMENTS/5_2025_11_Док_5_Глобальный.docx', 62500,
     'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
     '{"document_number": 5, "document_date": "2025-11", "topic": "global_platform", "has_attachments": true, "attachment_count": 1}',
     ARRAY['платформа', 'глобальный', '6ТУ']),

    ('SRC-ATT-004-1', '4_2025_11_Док_4_Приложение_1.pdf', 'Приложение 1 — Регуляторика + Суверенитет', 'RAW_SOURCES', 'immutable',
     'SOURCE_DOCUMENTS/4_2025_11_Док_4_Приложение_1.pdf', 2125000,
     'application/pdf',
     '{"parent_document": "SRC-DOC-004", "attachment_number": 1, "topic": "regulatory_sovereignty"}',
     ARRAY['регуляторика', 'суверенитет', 'нормативы']),

    ('SRC-ATT-004-2', '4_2025_11_Док_4_Приложение_2.pdf', 'Приложение 2 — Суверенитет', 'RAW_SOURCES', 'immutable',
     'SOURCE_DOCUMENTS/4_2025_11_Док_4_Приложение_2.pdf', 1850000,
     'application/pdf',
     '{"parent_document": "SRC-DOC-004", "attachment_number": 2, "topic": "sovereignty"}',
     ARRAY['суверенитет', 'технологический']),

    ('SRC-ATT-004-3', '4_2025_11_Док_4_Приложение_3.pdf', 'Приложение 3 — СЦИ', 'RAW_SOURCES', 'immutable',
     'SOURCE_DOCUMENTS/4_2025_11_Док_4_Приложение_3.pdf', 2350000,
     'application/pdf',
     '{"parent_document": "SRC-DOC-004", "attachment_number": 3, "topic": "sci_architecture"}',
     ARRAY['СЦИ', 'архитектура', 'инжиниринг']),

    ('SRC-ATT-004-4', '4_2025_11_Док_4_Приложение_4.xlsx', 'Приложение 4 — Рынок + CML-Bench', 'RAW_SOURCES', 'immutable',
     'SOURCE_DOCUMENTS/4_2025_11_Док_4_Приложение_4.xlsx', 285500,
     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
     '{"parent_document": "SRC-DOC-004", "attachment_number": 4, "topic": "market_cmlbench"}',
     ARRAY['рынок', 'CML-Bench', 'платформы']),

    ('SRC-ATT-004-5', '4_2025_11_Док_4_Приложение_5.pdf', 'Приложение 5 — CML-Bench детали', 'RAW_SOURCES', 'immutable',
     'SOURCE_DOCUMENTS/4_2025_11_Док_4_Приложение_5.pdf', 1756000,
     'application/pdf',
     '{"parent_document": "SRC-DOC-004", "attachment_number": 5, "topic": "cmlbench_details"}',
     ARRAY['CML-Bench', 'технология', 'детали']),

    ('SRC-ATT-005-1', '5_2025_11_Док_5_Приложение_1.pdf', 'Приложение Док5 — 6ТУ + Регуляторика', 'RAW_SOURCES', 'immutable',
     'SOURCE_DOCUMENTS/5_2025_11_Док_5_Приложение_1.pdf', 2135000,
     'application/pdf',
     '{"parent_document": "SRC-DOC-005", "attachment_number": 1, "topic": "6tu_regulatory"}',
     ARRAY['6ТУ', 'регуляторика', 'фундамент']),

    ('SRC-CHRONO', '2025_Хронология.docx', 'Хронология 2025', 'RAW_SOURCES', 'immutable',
     'SOURCE_DOCUMENTS/2025_Хронология.docx', 89879,
     'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
     '{"document_type": "chronology", "year": 2025, "topic": "timeline"}',
     ARRAY['хронология', 'timeline', '2025']),

    ('SRC-MKCP', 'МКЦП_редакция_после_МО.pdf', 'МКЦП — редакция после МО', 'RAW_SOURCES', 'immutable',
     'SOURCE_DOCUMENTS/МКЦП_редакция_после_МО.pdf', 2244000,
     'application/pdf',
     '{"document_type": "program", "topic": "mkcp_program", "budget_trillions": 15}',
     ARRAY['МКЦП', 'программа', 'ЦД']);

-- ============================================
-- ANALYTICAL NODES (13 узлов)
-- ============================================

INSERT INTO materials (material_id, filename, title, category, status, layer, file_path, file_size_bytes, mime_type, metadata, tags)
VALUES
    ('NODE-CONTEXT', 'psb_spbpu_context_analysis.json', 'Общий контекст Замысла ПСБ × СПбПУ', 'ANALYTICAL_NODES', 'production', 'L1-Strategic',
     'data/nodes/psb_spbpu_context_analysis.json', 69944, 'application/json',
     '{"node_type": "context", "importance": "high", "backlinks_count": 84}',
     ARRAY['контекст', 'ПСБ', 'СПбПУ', 'замысел']),

    ('NODE-SHAREHOLDER', 'psb_shareholder_logic_analysis.json', 'Логика акционера ПСБ', 'ANALYTICAL_NODES', 'production', 'L1-Strategic',
     'data/nodes/psb_shareholder_logic_analysis.json', 144063, 'application/json',
     '{"node_type": "shareholder", "importance": "high", "backlinks_count": 51}',
     ARRAY['акционер', 'ПСБ', 'логика', 'стратегия']),

    ('NODE-FINANCE', 'psb_financial_architecture_analysis.json', 'Финансовая архитектура', 'ANALYTICAL_NODES', 'production', 'L2-Operational',
     'data/nodes/psb_financial_architecture_analysis.json', 52143, 'application/json',
     '{"node_type": "finance", "importance": "high", "backlinks_count": 29}',
     ARRAY['финансы', 'архитектура', 'инвестиции']),

    ('NODE-ECOSYSTEM', 'psb_ecosystem_infrastructure_analysis.json', 'Экосистема и инфраструктура', 'ANALYTICAL_NODES', 'production', 'L2-Operational',
     'data/nodes/psb_ecosystem_infrastructure_analysis.json', 90560, 'application/json',
     '{"node_type": "ecosystem", "importance": "high", "backlinks_count": 35}',
     ARRAY['экосистема', 'инфраструктура', 'партнёрство']),

    ('NODE-TECHBASE', 'psb_technological_foundation_6tu_analysis.json', 'Технологический фундамент 6ТУ', 'ANALYTICAL_NODES', 'production', 'L3-Technical',
     'data/nodes/psb_technological_foundation_6tu_analysis.json', 81159, 'application/json',
     '{"node_type": "techbase", "importance": "high", "backlinks_count": 39}',
     ARRAY['6ТУ', 'технологии', 'фундамент']),

    ('NODE-PLATFORM', 'psb_global_trend_platform_analysis.json', 'Глобальный тренд — Платформа', 'ANALYTICAL_NODES', 'production', 'L1-Strategic',
     'data/nodes/psb_global_trend_platform_analysis.json', 45685, 'application/json',
     '{"node_type": "platform", "importance": "medium", "backlinks_count": 11}',
     ARRAY['платформа', 'глобальный', 'тренд']),

    ('NODE-REGULATORY', 'psb_regulatory_framework_analysis.json', 'Регуляторная рамка', 'ANALYTICAL_NODES', 'production', 'L2-Operational',
     'data/nodes/psb_regulatory_framework_analysis.json', 123906, 'application/json',
     '{"node_type": "regulatory", "importance": "medium", "backlinks_count": 7}',
     ARRAY['регуляторика', 'нормативы', 'законы']),

    ('NODE-SOVEREIGNTY', 'psb_strategic_sovereignty_role_analysis.json', 'Стратегический суверенитет', 'ANALYTICAL_NODES', 'production', 'L1-Strategic',
     'data/nodes/psb_strategic_sovereignty_role_analysis.json', 59203, 'application/json',
     '{"node_type": "sovereignty", "importance": "high", "backlinks_count": 15}',
     ARRAY['суверенитет', 'стратегия', 'независимость']),

    ('NODE-SCI', 'psb_sci_architecture_analysis.json', 'Архитектура СЦИ', 'ANALYTICAL_NODES', 'production', 'L3-Technical',
     'data/nodes/psb_sci_architecture_analysis.json', 43338, 'application/json',
     '{"node_type": "sci", "importance": "high", "backlinks_count": 16}',
     ARRAY['СЦИ', 'архитектура', 'инжиниринг']),

    ('NODE-MARKET', 'psb_dt_platforms_market_analysis.json', 'Рынок DT-платформ', 'ANALYTICAL_NODES', 'production', 'L2-Operational',
     'data/nodes/psb_dt_platforms_market_analysis.json', 55860, 'application/json',
     '{"node_type": "market", "importance": "medium", "backlinks_count": 12}',
     ARRAY['рынок', 'платформы', 'DT']),

    ('NODE-CMLBENCH', 'psb_cmlbench_technology_context_analysis.json', 'CML-Bench — технологический контекст', 'ANALYTICAL_NODES', 'production', 'L3-Technical',
     'data/nodes/psb_cmlbench_technology_context_analysis.json', 52350, 'application/json',
     '{"node_type": "cmlbench", "importance": "high", "backlinks_count": 10}',
     ARRAY['CML-Bench', 'технология', 'бенчмарк']),

    ('NODE-TIMELINE', 'psb_state_agenda_dt_timeline_analysis.json', 'Timeline государственной повестки DT', 'ANALYTICAL_NODES', 'production', 'L2-Operational',
     'data/nodes/psb_state_agenda_dt_timeline_analysis.json', 118530, 'application/json',
     '{"node_type": "timeline", "importance": "medium", "backlinks_count": 4}',
     ARRAY['timeline', 'государство', 'повестка']),

    ('NODE-MKCP', 'psb_mkcp_program_analysis.json', 'Программа МКЦП ЦД', 'ANALYTICAL_NODES', 'production', 'L1-Strategic',
     'data/nodes/psb_mkcp_program_analysis.json', 157496, 'application/json',
     '{"node_type": "mkcp", "importance": "critical", "backlinks_count": 0, "budget_trillions": 15, "period": "2026-2035"}',
     ARRAY['МКЦП', 'программа', 'ЦД', '15 трлн']);

-- ============================================
-- KNOWLEDGE GRAPH
-- ============================================

INSERT INTO materials (material_id, filename, title, category, status, file_path, file_size_bytes, mime_type, version, metadata, tags)
VALUES
    ('GRAPH-V14', 'psb_knowledge_graph_integration_v14.json', 'Knowledge Graph v14', 'KNOWLEDGE_GRAPH', 'production',
     'data/graph/psb_knowledge_graph_integration_v14.json', 201446, 'application/json', 'v14',
     '{"nodes_count": 13, "edges_count": 83, "total_backlinks": 313, "layers": 3}',
     ARRAY['граф', 'knowledge', 'v14']);

-- ============================================
-- SCHEMAS
-- ============================================

INSERT INTO materials (material_id, filename, title, category, status, file_path, file_size_bytes, mime_type, metadata, tags)
VALUES
    ('SCHEMA-JSON', 'psb_analytical_json_schema.json', 'JSON Schema для аналитических узлов', 'SCHEMAS', 'production',
     'data/schema/psb_analytical_json_schema.json', 5234, 'application/json',
     '{"schema_type": "json-schema", "validates": "analytical_nodes"}',
     ARRAY['schema', 'validation', 'json']),

    ('SCHEMA-ID', 'id_convention.json', 'Конвенция именования ID', 'SCHEMAS', 'production',
     'data/schema/id_convention.json', 2048, 'application/json',
     '{"schema_type": "convention", "purpose": "id_naming"}',
     ARRAY['convention', 'id', 'naming']);

-- ============================================
-- GOLD LAYER
-- ============================================

INSERT INTO materials (material_id, filename, title, category, status, file_path, file_size_bytes, mime_type, metadata, tags)
VALUES
    ('GOLD-MASTER', 'master_knowledge_base.json', 'Master Knowledge Base', 'GOLD', 'production',
     'data/gold/master_knowledge_base.json', 45000, 'application/json',
     '{"gold_type": "master", "total_materials": 62, "agent_entry_point": true}',
     ARRAY['gold', 'master', 'knowledge']),

    ('GOLD-AGENT', 'agent_schema.json', 'Knowledge Gate Agent Schema', 'GOLD', 'production',
     'data/gold/agent_schema.json', 8500, 'application/json',
     '{"gold_type": "agent", "agent_id": "AGENT-KNOWLEDGE-GATE"}',
     ARRAY['gold', 'agent', 'schema']),

    ('GOLD-INDEX', 'gold_index.json', 'Gold Index', 'GOLD', 'production',
     'data/gold/gold_index.json', 6500, 'application/json',
     '{"gold_type": "index", "purpose": "fast_lookup"}',
     ARRAY['gold', 'index', 'lookup']);

-- ============================================
-- ANALYTICAL NODES EXTENSION
-- ============================================

INSERT INTO analytical_nodes (id, node_id, layer, backlinks_count, outgoing_edges_count, source_ids, importance_score, centrality_score)
SELECT
    m.id,
    m.material_id,
    m.layer,
    (m.metadata->>'backlinks_count')::integer,
    CASE m.material_id
        WHEN 'NODE-CONTEXT' THEN 3
        WHEN 'NODE-SHAREHOLDER' THEN 4
        WHEN 'NODE-FINANCE' THEN 2
        WHEN 'NODE-ECOSYSTEM' THEN 1
        WHEN 'NODE-TECHBASE' THEN 4
        WHEN 'NODE-PLATFORM' THEN 8
        WHEN 'NODE-REGULATORY' THEN 6
        WHEN 'NODE-SOVEREIGNTY' THEN 7
        WHEN 'NODE-SCI' THEN 7
        WHEN 'NODE-MARKET' THEN 8
        WHEN 'NODE-CMLBENCH' THEN 10
        WHEN 'NODE-TIMELINE' THEN 11
        WHEN 'NODE-MKCP' THEN 12
        ELSE 0
    END,
    CASE m.material_id
        WHEN 'NODE-CONTEXT' THEN ARRAY['SRC-DOC-004']
        WHEN 'NODE-SHAREHOLDER' THEN ARRAY['SRC-DOC-001']
        WHEN 'NODE-FINANCE' THEN ARRAY['SRC-DOC-002']
        WHEN 'NODE-ECOSYSTEM' THEN ARRAY['SRC-DOC-003']
        WHEN 'NODE-TECHBASE' THEN ARRAY['SRC-ATT-005-1']
        WHEN 'NODE-PLATFORM' THEN ARRAY['SRC-DOC-005']
        WHEN 'NODE-REGULATORY' THEN ARRAY['SRC-ATT-004-1', 'SRC-ATT-005-1']
        WHEN 'NODE-SOVEREIGNTY' THEN ARRAY['SRC-ATT-004-1', 'SRC-ATT-004-2', 'SRC-DOC-004']
        WHEN 'NODE-SCI' THEN ARRAY['SRC-ATT-004-3']
        WHEN 'NODE-MARKET' THEN ARRAY['SRC-ATT-004-4']
        WHEN 'NODE-CMLBENCH' THEN ARRAY['SRC-ATT-004-4', 'SRC-ATT-004-5']
        WHEN 'NODE-TIMELINE' THEN ARRAY['SRC-CHRONO']
        WHEN 'NODE-MKCP' THEN ARRAY['SRC-MKCP']
        ELSE ARRAY[]::VARCHAR[]
    END,
    CASE m.material_id
        WHEN 'NODE-CONTEXT' THEN 0.95
        WHEN 'NODE-SHAREHOLDER' THEN 0.90
        WHEN 'NODE-TECHBASE' THEN 0.85
        WHEN 'NODE-ECOSYSTEM' THEN 0.80
        WHEN 'NODE-FINANCE' THEN 0.75
        WHEN 'NODE-MKCP' THEN 0.70
        ELSE 0.50
    END,
    CASE m.material_id
        WHEN 'NODE-CONTEXT' THEN 0.268  -- 84/313
        WHEN 'NODE-SHAREHOLDER' THEN 0.163
        WHEN 'NODE-TECHBASE' THEN 0.125
        WHEN 'NODE-ECOSYSTEM' THEN 0.112
        WHEN 'NODE-FINANCE' THEN 0.093
        ELSE 0.05
    END
FROM materials m
WHERE m.category = 'ANALYTICAL_NODES';

-- ============================================
-- SOURCE-NODE MAPPINGS
-- ============================================

INSERT INTO source_node_mapping (source_id, node_id, mapping_type, confidence)
SELECT
    s.id as source_id,
    n.id as node_id,
    'primary' as mapping_type,
    1.0 as confidence
FROM materials s
CROSS JOIN materials n
WHERE
    (s.material_id = 'SRC-DOC-001' AND n.material_id = 'NODE-SHAREHOLDER') OR
    (s.material_id = 'SRC-DOC-002' AND n.material_id = 'NODE-FINANCE') OR
    (s.material_id = 'SRC-DOC-003' AND n.material_id = 'NODE-ECOSYSTEM') OR
    (s.material_id = 'SRC-DOC-004' AND n.material_id = 'NODE-CONTEXT') OR
    (s.material_id = 'SRC-DOC-005' AND n.material_id = 'NODE-PLATFORM') OR
    (s.material_id = 'SRC-ATT-004-1' AND n.material_id = 'NODE-REGULATORY') OR
    (s.material_id = 'SRC-ATT-004-1' AND n.material_id = 'NODE-SOVEREIGNTY') OR
    (s.material_id = 'SRC-ATT-004-2' AND n.material_id = 'NODE-SOVEREIGNTY') OR
    (s.material_id = 'SRC-ATT-004-3' AND n.material_id = 'NODE-SCI') OR
    (s.material_id = 'SRC-ATT-004-4' AND n.material_id = 'NODE-MARKET') OR
    (s.material_id = 'SRC-ATT-004-4' AND n.material_id = 'NODE-CMLBENCH') OR
    (s.material_id = 'SRC-ATT-004-5' AND n.material_id = 'NODE-CMLBENCH') OR
    (s.material_id = 'SRC-ATT-005-1' AND n.material_id = 'NODE-TECHBASE') OR
    (s.material_id = 'SRC-ATT-005-1' AND n.material_id = 'NODE-REGULATORY') OR
    (s.material_id = 'SRC-CHRONO' AND n.material_id = 'NODE-TIMELINE') OR
    (s.material_id = 'SRC-MKCP' AND n.material_id = 'NODE-MKCP');

-- ============================================
-- Verify data loaded
-- ============================================

-- SELECT 'Materials loaded:' as info, COUNT(*) as count FROM materials;
-- SELECT 'Analytical nodes:' as info, COUNT(*) as count FROM analytical_nodes;
-- SELECT 'Source-node mappings:' as info, COUNT(*) as count FROM source_node_mapping;
