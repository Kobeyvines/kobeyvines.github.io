import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    // Use coerce to handle date strings from Obsidian/Python
    date: z.coerce.date(), 
    tags: z.array(z.string()).optional(),
    // ADD THESE THREE LINES
    readingTime: z.string().optional(),
    status: z.string().optional(),
    draft: z.boolean().optional().default(false),
  }),
});

const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    image: z.string().optional(),
    link: z.string().optional(),
    github: z.string().optional(),
    tags: z.array(z.string()).optional(),
    featured: z.boolean().optional().default(false),
    // ADD THIS LINE
    status: z.enum(['Live', 'In Progress', 'Archived']).default('In Progress'),
  }),
});

export const collections = { blog, projects };