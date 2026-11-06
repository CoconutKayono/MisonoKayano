using System.Collections;
using TMPro;
using UnityEngine;

public sealed class DialogueReveal : MonoBehaviour
{
    [SerializeField] private TMP_Text label;
    [SerializeField, Min(1f)] private float charactersPerSecond = 25f;
    private Coroutine reveal;

    public void Play(string content)
    {
        if (label == null) return;
        if (reveal != null) StopCoroutine(reveal);
        reveal = StartCoroutine(Reveal(content ?? string.Empty));
    }

    private IEnumerator Reveal(string content)
    {
        label.text = content;
        label.maxVisibleCharacters = 0;
        label.ForceMeshUpdate(); // Active text object; get current parsed count.
        int total = label.textInfo.characterCount;
        float shown = 0f;

        while (label.maxVisibleCharacters < total)
        {
            shown += Time.unscaledDeltaTime * Mathf.Max(1f, charactersPerSecond);
            label.maxVisibleCharacters = Mathf.Min(total, Mathf.FloorToInt(shown));
            yield return null;
        }

        label.maxVisibleCharacters = total;
        reveal = null;
    }

    private void OnDisable()
    {
        if (reveal != null) StopCoroutine(reveal);
        reveal = null;
    }
}
