/**
 * Logic executed by the n8n "Validate & Format Post" Code node.
 * Validates inputs from parallel branches (Gemini image + SEO hashtags) and Content Creator,
 * normalizes/deduplicates hashtags, and formats the payload for LinkedIn publishing.
 *
 * @param {Object} context
 * @param {Array} context.inputItems - Output items from Merge ($input.all())
 * @param {Object} context.contentCreatorOutput - Output object from $('Content creator').item.json.output
 * @param {Object} context.currentItemJson - $json of the current merged item
 * @param {Object} context.currentItemBinary - $binary of the current merged item
 * @returns {Array<{ json: Object, binary: Object }>}
 */
function validateAndFormatPost({
  inputItems,
  contentCreatorOutput = {},
  currentItemJson = {},
  currentItemBinary = {}
}) {
  if (!Array.isArray(inputItems) || inputItems.length !== 1) {
    throw new Error(
      `Validation failed: expected exactly 1 merged item from parallel branches, received ${
        Array.isArray(inputItems) ? inputItems.length : 0
      }.`
    );
  }

  const rawTitle = String(contentCreatorOutput['post title'] || '').trim();
  const rawContent = String(contentCreatorOutput['post content'] || '').trim();

  if (!rawTitle) {
    throw new Error('Validation failed: post title is empty or missing.');
  }

  if (!rawContent) {
    throw new Error('Validation failed: post content is empty or missing.');
  }

  const binaryKeys = Object.keys(currentItemBinary || {});
  const imageKey = currentItemBinary?.data ? 'data' : binaryKeys[0];

  if (!imageKey || !currentItemBinary[imageKey]) {
    throw new Error(
      'Validation failed: missing binary image data in item.binary from Gemini Image Generator.'
    );
  }

  // Strip accidental hashtag lines from post copy
  const cleanBody = rawContent
    .split('\n')
    .filter((line) => !line.trim().startsWith('#'))
    .join('\n')
    .trim();

  const rawHashtags = Array.isArray(currentItemJson.output?.Hashtags)
    ? currentItemJson.output.Hashtags
    : [];

  const seen = new Set();
  const normalizedHashtags = [];

  for (const entry of rawHashtags) {
    const parts = String(entry || '').split(/[,\s]+/);
    for (let tag of parts) {
      tag = tag.trim().replace(/^#+/, '').replace(/[^a-zA-Z0-9_]/g, '');
      if (!tag) continue;
      const formatted = '#' + tag;
      const lower = formatted.toLowerCase();
      if (!seen.has(lower)) {
        seen.add(lower);
        normalizedHashtags.push(formatted);
      }
    }
  }

  const formattedText =
    normalizedHashtags.length > 0
      ? cleanBody + '\n\n' + normalizedHashtags.join(' ')
      : cleanBody;

  return [
    {
      json: {
        formattedTitle: rawTitle,
        formattedText,
        normalizedHashtags
      },
      binary: {
        data: currentItemBinary[imageKey]
      }
    }
  ];
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { validateAndFormatPost };
}
