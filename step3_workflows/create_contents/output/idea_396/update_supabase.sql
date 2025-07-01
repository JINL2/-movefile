
-- 1. contents_idea 테이블 업데이트 (is_fetched = true)
UPDATE contents_idea 
SET 
    is_fetched = true,
    custom_idea_metadata = '{"idea_id": 396, "processed_at": "2025-07-01T16:07:37.116088", "title": "테스트 한국어 제목 - 2025. 7. 1. 오후 3:43:12", "script": {"title": "테스트 한국어 제목 - 2025. 7. 1. 오후 3:43:12", "scenes": [{"type": "hook", "number": 1, "content": "테스트 훅 1", "duration": 3}, {"type": "body", "number": 1, "content": "테스트 본문 1", "duration": 10}, {"type": "hook", "number": 2, "content": "테스트 훅 2", "duration": 3}, {"type": "body", "number": 2, "content": "테스트 본문 2", "duration": 10}, {"type": "conclusion", "content": "테스트 결론", "duration": 5}]}, "visuals": {"thumbnail": "thumbnail_idea_396.jpg", "images": ["scene_1_idea_396.jpg", "scene_2_idea_396.jpg"], "video": "content_idea_396.mp4"}, "captions": {"main_caption": "테스트 한국어 제목 - 2025. 7. 1. 오후 3:43:12 - Test Vietnamese Title - 2025. 7. 1. 오후 3:43:12", "hashtags": ["#콘텐츠", "#아이디어", "#idea_396", "#viral", "#trending"], "platform_specific": {"tiktok": "TikTok용 짧은 캡션", "instagram": "Instagram용 긴 캡션"}}, "optimizations": {"tiktok": {"aspect_ratio": "9:16", "max_duration": 60, "format": "mp4"}, "instagram": {"aspect_ratio": "1:1", "max_duration": 90, "format": "mp4"}}}'::jsonb
WHERE id = 396;

-- 2. 워크플로우 처리 결과 로그 테이블 생성 (없으면)
CREATE TABLE IF NOT EXISTS workflow_logs (
    id SERIAL PRIMARY KEY,
    idea_id INTEGER REFERENCES contents_idea(id),
    processed_at TIMESTAMP DEFAULT NOW(),
    workflow_type VARCHAR(100),
    status VARCHAR(50),
    result_metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 3. 워크플로우 로그 삽입
INSERT INTO workflow_logs (idea_id, workflow_type, status, result_metadata)
VALUES (396, 'create_contents', 'completed', '{"idea_id": 396, "processed_at": "2025-07-01T16:07:37.116088", "title": "테스트 한국어 제목 - 2025. 7. 1. 오후 3:43:12", "script": {"title": "테스트 한국어 제목 - 2025. 7. 1. 오후 3:43:12", "scenes": [{"type": "hook", "number": 1, "content": "테스트 훅 1", "duration": 3}, {"type": "body", "number": 1, "content": "테스트 본문 1", "duration": 10}, {"type": "hook", "number": 2, "content": "테스트 훅 2", "duration": 3}, {"type": "body", "number": 2, "content": "테스트 본문 2", "duration": 10}, {"type": "conclusion", "content": "테스트 결론", "duration": 5}]}, "visuals": {"thumbnail": "thumbnail_idea_396.jpg", "images": ["scene_1_idea_396.jpg", "scene_2_idea_396.jpg"], "video": "content_idea_396.mp4"}, "captions": {"main_caption": "테스트 한국어 제목 - 2025. 7. 1. 오후 3:43:12 - Test Vietnamese Title - 2025. 7. 1. 오후 3:43:12", "hashtags": ["#콘텐츠", "#아이디어", "#idea_396", "#viral", "#trending"], "platform_specific": {"tiktok": "TikTok용 짧은 캡션", "instagram": "Instagram용 긴 캡션"}}, "optimizations": {"tiktok": {"aspect_ratio": "9:16", "max_duration": 60, "format": "mp4"}, "instagram": {"aspect_ratio": "1:1", "max_duration": 90, "format": "mp4"}}}'::jsonb);
