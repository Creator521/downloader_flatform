import os
import importlib.util

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
                        # Prefer slug from the dict, otherwise infer from filename
                        slug = post_data.get('slug', module_name.replace('_', '-'))
                        BLOG_POSTS[slug] = post_data
                except Exception as e:
                    pass
