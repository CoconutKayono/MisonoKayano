> 原文：[MonoBehaviour.OnAudioFilterRead](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.OnAudioFilterRead.html)

# [MonoBehaviour](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/MonoBehaviour.html).OnAudioFilterRead

## 声明

~~~csharp
public void OnAudioFilterRead(...);
~~~

## 参数

| 参数 | 描述 |
| --- | --- |
| data | An array of floats comprising the audio data. |
| channels | An int that stores the number of channels of audio data passed to this delegate. |

## 描述

如果实现 OnAudioFilterRead，Unity 会在音频 DSP 链中插入自定义滤波器。

## 示例

~~~csharp
using UnityEngine;

// The code example shows how to implement a metronome that procedurally
// generates the click sounds via the OnAudioFilterRead callback.
// While the game is paused or suspended, this time will not be updated and sounds
// playing will be paused. Therefore developers of music scheduling routines do not have
// to do any rescheduling after the app is unpaused

[ RequireComponent (typeof( AudioSource ))]
public class AudioTest :  MonoBehaviour 
{
    public double bpm = 140.0F;
    public float gain = 0.5F;
    public int signatureHi = 4;
    public int signatureLo = 4;

    private double nextTick = 0.0F;
    private float amp = 0.0F;
    private float phase = 0.0F;
    private double sampleRate = 0.0F;
    private int accent;
    private bool running = false;

    void Start()
    {
        accent = signatureHi;
        double startTick =  AudioSettings.dspTime ;
        sampleRate =  AudioSettings.outputSampleRate ;
        nextTick = startTick * sampleRate;
        running = true;
    }

    void OnAudioFilterRead(float[] data, int channels)
    {
        if (!running)
            return;

        double samplesPerTick = sampleRate * 60.0F / bpm * 4.0F / signatureLo;
        double sample =  AudioSettings.dspTime  * sampleRate;
        int dataLen = data.Length / channels;

        int n = 0;
        while (n < dataLen)
        {
            float x = gain * amp *  Mathf.Sin (phase);
            int i = 0;
            while (i < channels)
            {
                data[n * channels + i] += x;
                i++;
            }
            while (sample + n >= nextTick)
            {
                nextTick += samplesPerTick;
                amp = 1.0F;
                if (++accent > signatureHi)
                {
                    accent = 1;
                    amp *= 2.0F;
                }
                 Debug.Log ("Tick: " + accent + "/" + signatureHi);
            }
            phase += amp * 0.3F;
            amp *= 0.993F;
            n++;
        }
    }
}
~~~

## 相关资源

- [Audio Filters](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/../Manual/class-AudioEffect.html)

---

## 文档导航

- 上一页：[[18-OnApplicationQuit]]
- 目录：[[00-MonoBehaviour]]
- 下一页：[[20-OnBecameInvisible]]







