using TMPro;
using UnityEngine;

public sealed class ScoreLabel : MonoBehaviour
{
    [SerializeField] private TMP_Text label;
    private int lastScore;
    private bool hasScore;

    public void SetScore(int score)
    {
        if (label == null || (hasScore && score == lastScore))
            return;

        hasScore = true;
        lastScore = score;
        label.SetText("分数：{0:0}", (float)score);
    }
}
