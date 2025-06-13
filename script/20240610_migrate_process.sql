-- Create migrate_process table
CREATE TABLE IF NOT EXISTS migrate_process (
    id SERIAL PRIMARY KEY,
    quiz_id VARCHAR(255) NOT NULL,
    status INTEGER NOT NULL DEFAULT 1,
    
    -- Trạng thái và kết quả của bước Prepare Data
    prepare_data_status VARCHAR(50) NOT NULL DEFAULT 'pending',
    prepare_data_result JSONB,
    prepare_data_error VARCHAR(1000),
    
    -- Trạng thái và kết quả của bước Mapping Structure
    mapping_structure_status VARCHAR(50) NOT NULL DEFAULT 'pending',
    mapping_structure_result JSONB,
    mapping_structure_error VARCHAR(1000),
    
    -- Trạng thái và kết quả của bước Validate Data
    validate_data_status VARCHAR(50) NOT NULL DEFAULT 'pending',
    validate_data_result JSONB,
    validate_data_error VARCHAR(1000),
    
    -- Kết quả cuối cùng
    result JSONB,
    error_message VARCHAR(1000),
    
    date_created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
