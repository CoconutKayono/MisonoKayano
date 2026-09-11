# ScriptableObject 类

> 原文：[ScriptableObject](https://docs.unity3d.com/6000.7/Documentation/Manual/class-ScriptableObject.html)

`ScriptableObject` 是一种可序列化的 Unity 类型，继承自 `UnityEngine.Object`。与 `MonoBehaviour` 一样，不要直接实例化 `ScriptableObject` 类，而应创建继承它的自定义 C# 类，再创建这些自定义类的实例，通常通过 Unity Editor 中的 **Assets** 菜单完成。

所有派生自 `ScriptableObject` 的类实例通常都称为 ScriptableObject。与 `MonoBehaviour` 不同，ScriptableObject 不会作为 Component 附加到 `GameObject` 上，而是作为独立于 `GameObject` 的 Asset 存在于项目中。由于它们继承自 `UnityEngine.Object`，可以将 ScriptableObject 实例拖放到 Inspector 的字段中，或使用 Object Picker 选择它们。

ScriptableObject 的主要价值是充当数据存储，也可以定义行为。常见用途是保存多个对象在 Runtime 共享的数据，通过避免复制值来降低项目的内存使用量。

例如，如果 Prefab 在附加的 `MonoBehaviour` 脚本中保存不变数据，每个新的 Prefab 实例都会获得一份数据副本。可以改用 ScriptableObject 存储数据，再让所有 Prefab 通过引用访问它，这样内存中只需要一份数据。

ScriptableObject 的主要使用场景包括：

- 在 Editor Session 期间保存和存储数据。因此，Unity 中许多创作工具（例如 `EditorTool` 和 `EditorWindow`）都继承自 ScriptableObject。
- 将数据保存为项目 Asset，以便在 Runtime 使用。

ScriptableObject 类的完整成员参考，请参阅 [ScriptableObject API 参考](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/ScriptableObject.html)。

## 创建 ScriptableObject

创建新的 ScriptableObject 脚本，最快的方式是使用预定义的 ScriptableObject 脚本模板：

- 在主菜单中选择 **Assets > Create > Scripting > ScriptableObject Script**。
- 在 Project 窗口中右键打开上下文菜单，选择 **Create > Scripting > ScriptableObject Script**。也可以点击 Project 窗口中的加号，直接打开 Create 菜单。

这会创建一个继承自 `UnityEngine.ScriptableObject` 的自定义基类。随后可以使用 `CreateAssetMenu` Attribute 创建该类的实例，每个实例都会成为项目中的一个 Asset。

## 示例：使用 ScriptableObject 实例化 Prefab

下面的示例使用 ScriptableObject 保存创作阶段定义的数据，并在 Runtime 根据这些数据决定 Prefab 的实例化位置。首先，在 `Assets` 文件夹中创建以下基础 ScriptableObject 类：

```csharp
using UnityEngine;

// 使用 CreateAssetMenu，让 Unity Editor 可以创建此 ScriptableObject 的实例。
[CreateAssetMenu(
    fileName = "Data",
    menuName = "ScriptableObjects/SpawnManagerScriptableObject",
    order = 1)]
public class SpawnManagerScriptableObject : ScriptableObject
{
    public string prefabName;
    public int numberOfPrefabsToCreate;
    public Vector3[] spawnPoints;
}
```

将脚本放入 `Assets` 文件夹后，选择 **Assets > Create > ScriptableObjects > SpawnManagerScriptableObject**，创建新 ScriptableObject 实例。为实例设置有意义的名称，并修改其中的值。

要在 Runtime 使用这些值，需要创建一个引用该 ScriptableObject 的新脚本：

```csharp
using UnityEngine;

public class ScriptableObjectManagedSpawner : MonoBehaviour
{
    // 要实例化的 GameObject。
    public GameObject entityToSpawn;

    // 上面定义的 ScriptableObject 实例。
    public SpawnManagerScriptableObject spawnManagerValues;

    // 添加到创建对象名称末尾的编号，每次创建后递增。
    int instanceNumber = 1;

    void Start()
    {
        SpawnEntities();
    }

    void SpawnEntities()
    {
        int currentSpawnPointIndex = 0;

        for (int i = 0; i < spawnManagerValues.numberOfPrefabsToCreate; i++)
        {
            // 在当前生成点实例化 Prefab。
            GameObject currentEntity = Instantiate(
                entityToSpawn,
                spawnManagerValues.spawnPoints[currentSpawnPointIndex],
                Quaternion.identity);

            // 使用 ScriptableObject 中的字符串命名实例，并追加唯一编号。
            currentEntity.name = spawnManagerValues.prefabName + instanceNumber;

            // 移动到下一个生成点索引；超出范围时回到开头。
            currentSpawnPointIndex =
                (currentSpawnPointIndex + 1) % spawnManagerValues.spawnPoints.Length;

            instanceNumber++;
        }
    }
}
```

> [!NOTE]
> 脚本文件名必须与类名相同。

将上面的脚本附加到 Scene 中的 `GameObject`。然后在 Inspector 中，将新创建的 `SpawnManagerScriptableObject` `.asset` 实例拖入 **Spawn Manager Values** 字段。

将 `Assets` 文件夹中的任意 Prefab 拖入 **Entity To Spawn** 字段，然后进入 Play Mode。`ScriptableObjectManagedSpawner` 会按照 `SpawnManagerScriptableObject` 实例中设置的值实例化 Prefab。

在 Inspector 中使用 ScriptableObject 引用时，可以双击引用字段，打开该 ScriptableObject 的 Inspector。也可以为自己的类型创建自定义 Inspector，以便管理它所表示的数据。

## 保存 ScriptableObject 数据的更改

在 Unity Editor 中，可以在 Edit Mode 和 Play Mode 中保存 ScriptableObject 数据。在 Runtime 运行的独立 Player 中，只能读取 ScriptableObject Asset 中已保存的数据。当通过 Editor 创作工具或 Inspector 修改 ScriptableObject Asset 时，Unity 会自动将数据写入磁盘，并在不同 Editor Session 之间保留数据。

但是，在 Edit Mode 中通过脚本修改 ScriptableObject 时，Unity 不会自动保存更改。此时必须对 ScriptableObject 调用 `EditorUtility.SetDirty`，确保 Unity 序列化系统识别到它已更改并将更改保存到磁盘。否则，更改可能不会在不同 Editor Session 之间保留。

下面是一个用于存储游戏设置的简单 ScriptableObject：

```csharp
using UnityEngine;

[CreateAssetMenu(
    fileName = "GameSettings",
    menuName = "ScriptableObjects/GameSettingsScriptableObject",
    order = 2)]
public class GameSettingsScriptableObject : ScriptableObject
{
    public int highScore;
}
```

通过 **Assets > Create > ScriptableObjects > GameSettingsScriptableObject** 在项目中创建该类的实例，然后在 Inspector 中设置 `highScore` 值。

下面的 Editor 脚本会添加一个简单窗口，其中的按钮可以增加最高分。窗口位于 **Window > Game Settings Editor**：

```csharp
using UnityEditor;
using UnityEngine;

public class GameSettingsEditor : EditorWindow
{
    GameSettingsScriptableObject settings;

    // 创建一个用于修改 ScriptableObject 最高分的简单 Editor Window。
    // 入口：Window > Game Settings Editor
    [MenuItem("Window/Game Settings Editor")]
    public static void ShowWindow()
    {
        GetWindow<GameSettingsEditor>("Game Settings Editor");
    }

    void OnGUI()
    {
        settings = EditorGUILayout.ObjectField(
            "Settings",
            settings,
            typeof(GameSettingsScriptableObject),
            false) as GameSettingsScriptableObject;

        if (settings == null)
            return;

        EditorGUILayout.LabelField("High Score", settings.highScore.ToString());

        // 点击 Increase High Score 按钮，将最高分增加 10。
        if (GUILayout.Button("Increase High Score"))
        {
            settings.highScore += 10;

            // 确保更改被保存。
            EditorUtility.SetDirty(settings);

            // 可选：立即保存。
            // AssetDatabase.SaveAssets();
        }
    }
}
```

如果省略本例中的 `EditorUtility.SetDirty` 调用，`highScore` 的更改会暂时出现在内存中，但关闭并重新打开 Editor 后，数值会恢复为之前的值。

---

## 文档导航

- 上一页：[[02-MonoBehaviour类]]
- 目录：[[00-Unity基础类型]]
- 下一页：[[04-Unity属性]]
