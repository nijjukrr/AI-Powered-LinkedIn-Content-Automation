const { test, describe } = require('node:test');
const assert = require('node:assert/strict');
const { validateAndFormatPost } = require('../scripts/validate_format_post.js');

describe('Validate & Format Post (Node.js direct execution tests)', () => {
  const validBinary = {
    data: {
      data: 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==',
      mimeType: 'image/png',
      fileName: 'post-image.png'
    }
  };

  const validCreator = {
    'post title': 'Mastering Internships as a Student',
    'post content': 'Here is actionable career advice for students.\n#badtag\nFocus on real projects and clear problem statements.'
  };

  test('happy path: formats title, strips inline hashtags, normalizes and dedupes hashtags, preserves binary.data', () => {
    const inputItems = [{ json: {}, binary: validBinary }];
    const currentItemJson = {
      output: {
        Hashtags: ['#SoftwareEngineering', 'TECH, #internships', '#softwareengineering', '###AI_2026!']
      }
    };

    const result = validateAndFormatPost({
      inputItems,
      contentCreatorOutput: validCreator,
      currentItemJson,
      currentItemBinary: validBinary
    });

    assert.equal(result.length, 1);
    assert.equal(result[0].json.formattedTitle, 'Mastering Internships as a Student');
    assert.equal(
      result[0].json.formattedText,
      'Here is actionable career advice for students.\nFocus on real projects and clear problem statements.\n\n#SoftwareEngineering #TECH #internships #AI_2026'
    );
    assert.deepEqual(result[0].json.normalizedHashtags, [
      '#SoftwareEngineering',
      '#TECH',
      '#internships',
      '#AI_2026'
    ]);
    assert.ok(result[0].binary.data);
    assert.equal(result[0].binary.data.mimeType, 'image/png');
  });

  test('throws error if post title is missing or empty', () => {
    const inputItems = [{ json: {}, binary: validBinary }];
    assert.throws(
      () =>
        validateAndFormatPost({
          inputItems,
          contentCreatorOutput: { 'post title': '', 'post content': 'valid content' },
          currentItemJson: { output: { Hashtags: [] } },
          currentItemBinary: validBinary
        }),
      /post title is empty or missing/
    );
  });

  test('throws error if post content is missing or empty', () => {
    const inputItems = [{ json: {}, binary: validBinary }];
    assert.throws(
      () =>
        validateAndFormatPost({
          inputItems,
          contentCreatorOutput: { 'post title': 'valid title', 'post content': '   ' },
          currentItemJson: { output: { Hashtags: [] } },
          currentItemBinary: validBinary
        }),
      /post content is empty or missing/
    );
  });

  test('throws error if binary image data is missing', () => {
    const inputItems = [{ json: {}, binary: {} }];
    assert.throws(
      () =>
        validateAndFormatPost({
          inputItems,
          contentCreatorOutput: validCreator,
          currentItemJson: { output: { Hashtags: [] } },
          currentItemBinary: {}
        }),
      /missing binary image data/
    );
  });

  test('normalizes binary property if named under alternate key', () => {
    const customBinary = {
      image: {
        data: 'base64sample',
        mimeType: 'image/jpeg'
      }
    };
    const inputItems = [{ json: {}, binary: customBinary }];
    const result = validateAndFormatPost({
      inputItems,
      contentCreatorOutput: validCreator,
      currentItemJson: { output: { Hashtags: ['#Career'] } },
      currentItemBinary: customBinary
    });

    assert.ok(result[0].binary.data, 'Should normalize key to binary.data for LinkedIn node');
    assert.equal(result[0].binary.data.mimeType, 'image/jpeg');
  });

  test('throws error if inputItems count is not exactly 1', () => {
    assert.throws(
      () =>
        validateAndFormatPost({
          inputItems: [],
          contentCreatorOutput: validCreator,
          currentItemJson: {},
          currentItemBinary: validBinary
        }),
      /expected exactly 1 merged item from parallel branches, received 0/
    );

    assert.throws(
      () =>
        validateAndFormatPost({
          inputItems: [{}, {}],
          contentCreatorOutput: validCreator,
          currentItemJson: {},
          currentItemBinary: validBinary
        }),
      /expected exactly 1 merged item from parallel branches, received 2/
    );
  });

  test('handles empty or missing hashtag array gracefully without trailing newlines', () => {
    const inputItems = [{ json: {}, binary: validBinary }];
    const result = validateAndFormatPost({
      inputItems,
      contentCreatorOutput: { 'post title': 'Title Only', 'post content': 'Pure content text.' },
      currentItemJson: { output: { Hashtags: [] } },
      currentItemBinary: validBinary
    });

    assert.equal(result[0].json.formattedText, 'Pure content text.');
    assert.deepEqual(result[0].json.normalizedHashtags, []);
  });
});
