# Topaz Photo AI integration

This extension integrates [Topaz Photo AI](https://www.topazlabs.com/topaz-photo-ai) upscaling feature into [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui). So you can use it inside *hires fix*, *upscaler_for_img2img* or in *extras* tab. You need to have Topaz Photo AI of version >= 2.1.3 (do not confuse with topaz gigapixel), and provide a path to `tpai.exe` usually located in `C:\Program Files\Topaz Labs LLC\Topaz Photo AI` in `Settings/Upscaling` of webui

![](/images/preview.png)
![](/images/upscalers.png)

To copy path to file in Windows, you need to press right mouse click holding "Shift" button, and select "Copy file as path"


If you use Linux, you need to write a script, which launches `tpai.exe` via wine, with all arguments passing. E.g.

```bash
#!/bin/bash
cd "$(dirname "$0")"
wine <path to tpai.exe> "$@"
rc=$?
exit $rc
```

You also need to install `winetricks` and run `winetricks -q dxvk` to allow topaz to see your gpu


<details>
<summary>
For portable version
</summary>

If you use a portable version of Topaz Photo AI, you need to write a wrapper script which replaces `Topaz Photo AI.exe` with `tpai.exe` and starts portable version, and set path to this script instead

For Linux:
```bash
#!/bin/bash
cd "$(dirname "$0")"
export WINEDEBUG=-all
mv 'App/Topaz Photo AI/Topaz Photo AI.exe' 'App/Topaz Photo AI/Topaz Photo AI_.exe'
mv 'App/Topaz Photo AI/tpai.exe' 'App/Topaz Photo AI/Topaz Photo AI.exe'
xvfb-run wine PhotoAIportable.exe "$@"
rc=$?
mv 'App/Topaz Photo AI/Topaz Photo AI.exe' 'App/Topaz Photo AI/tpai.exe'
mv 'App/Topaz Photo AI/Topaz Photo AI_.exe' 'App/Topaz Photo AI/Topaz Photo AI.exe'
exit $rc
```

`xvfb-run` is not necessary, it's used for hiding cmd.exe window. Can be installed by `sudo yay -S xorg-server-xvfb` on Arch-based, or `sudo apt install xvfb` on Ubuntu-based

Or for Windows (I'm not sure, converted by AI)
```bat
@echo off
setlocal
cd /d "%~dp0"
move "App\Topaz Photo AI\Topaz Photo AI.exe" "App\Topaz Photo AI\Topaz Photo AI_.exe"
move "App\Topaz Photo AI\tpai.exe" "App\Topaz Photo AI\Topaz Photo AI.exe"
start /wait /min "" cmd /c "PhotoAIportable.exe %*"
set rc=%errorlevel%
move "App\Topaz Photo AI\Topaz Photo AI.exe" "App\Topaz Photo AI\tpai.exe"
move "App\Topaz Photo AI\Topaz Photo AI_.exe" "App\Topaz Photo AI\Topaz Photo AI.exe"
exit /b %rc%
```

</details>

Btw this extension is more about fun, and adding topaz in webui just because it's possibe. If you want to get models with similar quality, you can use [4x-Nomos8kHAT-L-otf](https://openmodeldb.info/models/4x-Nomos8kHAT-L-otf) and [4x-FaceUpDAT](https://openmodeldb.info/models/4x-FaceUpDAT), place them into `models/DAT` directory, or even you can try [StableSR](https://github.com/pkuliyi2015/sd-webui-stablesr)

Btw in some cases Topaz shows the best quality:
![](/images/comparation.jpg)


