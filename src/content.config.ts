import { z, defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';

const chapterCollection = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/ebook" }),
  schema: z.object({
    chapter: z.number(),
    slug: z.string().optional(),
    title: z.string(),
    subtitle: z.string().optional(),
    part: z.union([z.number(), z.string()]).optional(),
    status: z.enum(['draft', 'published', 'revised', 'canonical']).default('draft'),
    edition: z.number().optional(),
    published_at: z.date().optional(),
    updated_at: z.date().optional(),
    language: z.enum(['en', 'es']).default('en'),
    summary: z.string(),
    reading_time: z.string().optional(),
    topics: z.array(z.string()).optional(),
    hero_image: z.string().optional(),
    linkedin_summary_url: z.string().optional()
  }),
});

export const collections = {
  'ebook': chapterCollection,
};
