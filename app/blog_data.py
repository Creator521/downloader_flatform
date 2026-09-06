import logging
import os
import importlib.util

logger = logging.getLogger(__name__)

BLOG_POSTS = {}

current_dir = os.path.dirname(os.path.abspath(__file__))
blog_posts_dir = os.path.join(current_dir, "blog_posts")

if os.path.exists(blog_posts_dir):
    files = os.listdir(blog_posts_dir)
    for filename in files:
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            file_path = os.path.join(blog_posts_dir, filename)
            
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                    if hasattr(module, 'post'):
                        post_data = module.post
                        # Normalize: support both 'meta_description' and 'description' keys
                        # Template uses post.description, but newer posts use meta_description
                        if 'meta_description' in post_data and 'description' not in post_data:
                            post_data['description'] = post_data['meta_description']
                        # E-E-A-T: replace the generic 'Admin' byline with the
                        # editorial team name shown in the author bio box
                        if not post_data.get('author') or str(post_data['author']).strip().lower() in ('admin', 'administrator'):
                            post_data['author'] = 'SnapReelDownload Team'
                        # Prefer slug from the dict, otherwise infer from filename
                        slug = post_data.get('slug', module_name.replace('_', '-'))
                        post_data['slug'] = slug  # Ensure slug is always in the dict
                        BLOG_POSTS[slug] = post_data
                except Exception as e:
                    # Never silently drop a post — a syntax error here makes the
                    # article 404 with no trace in the logs
                    logger.error("Failed to load blog post %s: %s", filename, e)
