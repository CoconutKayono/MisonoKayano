Shader "FAQ/SpaceAwareness"
{
    Properties
    {
        [Enum(ObjectStripes,0,WorldStripes,1,WorldNormal,2,WrongNormal,3,ScreenStripes,4,NormalError,5)]
        _Mode("Mode", Float) = 0
        _Frequency("Frequency", Range(0.1, 24)) = 3
        _Dark("Dark", Color) = (0.04, 0.08, 0.15, 1)
        _Light("Light", Color) = (0.15, 0.85, 0.75, 1)
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" "RenderPipeline"="UniversalPipeline" "Queue"="Geometry" }
        Pass
        {
            Name "SpaceAwareness"
            Tags { "LightMode"="SRPDefaultUnlit" }
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

            CBUFFER_START(UnityPerMaterial)
                float4 _Dark;
                float4 _Light;
                float _Mode;
                float _Frequency;
            CBUFFER_END

            struct Attributes
            {
                float4 positionOS : POSITION;
                float3 normalOS : NORMAL;
            };

            struct Varyings
            {
                float4 positionCS : SV_POSITION;
                float3 positionOS : TEXCOORD0;
                float3 positionWS : TEXCOORD1;
                float3 normalWS : TEXCOORD2;
                float3 wrongNormalWS : TEXCOORD3;
            };

            Varyings vert(Attributes IN)
            {
                Varyings OUT;
                OUT.positionCS = TransformObjectToHClip(IN.positionOS.xyz);
                OUT.positionOS = IN.positionOS.xyz;
                OUT.positionWS = TransformObjectToWorld(IN.positionOS.xyz);
                OUT.normalWS = TransformObjectToWorldNormal(IN.normalOS);
                // Deliberately wrong: compare with inverse-transpose normal transform.
                OUT.wrongNormalWS = mul((float3x3)GetObjectToWorldMatrix(), IN.normalOS);
                return OUT;
            }

            half4 frag(Varyings IN) : SV_Target
            {
                float3 n = normalize(IN.normalWS);
                float3 wrongN = normalize(IN.wrongNormalWS);
                if (_Mode > 4.5)
                {
                    float error = saturate(length(n - wrongN) * 2.0);
                    return half4(error, 0, 0, 1);
                }
                if (_Mode > 1.5 && _Mode < 3.5)
                {
                    float3 shownN = _Mode < 2.5 ? n : wrongN;
                    return half4(shownN * 0.5 + 0.5, 1);
                }
                float coordinate = _Mode < 0.5 ? IN.positionOS.y : IN.positionWS.y;
                if (_Mode > 3.5)
                {
                    // Fragment SV_POSITION.xy is pixel position, not original clip.xy.
                    coordinate = GetNormalizedScreenSpaceUV(IN.positionCS.xy).y;
                }
                float phase = coordinate * _Frequency;
                float wave = sin(phase * 6.28318530718);
                float edgeWidth = max(fwidth(wave), 0.001);
                float stripe = smoothstep(-edgeWidth, edgeWidth, wave);
                return half4(lerp(_Dark.rgb, _Light.rgb, stripe), 1);
            }
            ENDHLSL
        }
    }
}
