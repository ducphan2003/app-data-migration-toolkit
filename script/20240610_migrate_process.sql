-- Create migrate_process table
CREATE TABLE IF NOT EXISTS migrate_process (
    id SERIAL PRIMARY KEY,
    quiz_id VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'processing',
    prepare_data_status VARCHAR(20) DEFAULT 'pending',
    prepare_data_result TEXT,
    mapping_structure_status VARCHAR(20) DEFAULT 'pending',
    mapping_structure_result TEXT,
    validate_data_status VARCHAR(20) DEFAULT 'pending',
    validate_data_result TEXT,
    final_result TEXT,
    error_message TEXT,
    user_created VARCHAR(50) NOT NULL,
    date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP
);
