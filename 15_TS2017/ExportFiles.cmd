@echo off
set TARGETLANGUAGES=%~1


call TS2015 Export-TargetFiles ^
  -ProjectLocation "DE" ^
  -ExportLocation "_GeneratedFilesFlat" ^
  -TargetLanguages "%TARGETLANGUAGES%"

call TS2015 Export-TargetFiles ^
  -ProjectLocation "ES" ^
  -ExportLocation "_GeneratedFilesFlat" ^
  -TargetLanguages "%TARGETLANGUAGES%"

call TS2015 Export-TargetFiles ^
  -ProjectLocation "FR" ^
  -ExportLocation "_GeneratedFilesFlat" ^
  -TargetLanguages "%TARGETLANGUAGES%"

call TS2015 Export-TargetFiles ^
  -ProjectLocation "FRCA" ^
  -ExportLocation "_GeneratedFilesFlat" ^
  -TargetLanguages "%TARGETLANGUAGES%"

FOR %%G IN (de-de es-es fr-fr fr-ca) DO (
copy kopiruj.bat _GeneratedFilesFlat\%%G
robocopy temp _GeneratedFilesFlat\%%G\temp /E
cd _GeneratedFilesFlat\%%G
call kopiruj.bat
cd..
cd..
robocopy _GeneratedFilesFlat\%%G\temp "..\50_toClient\Generated Files\%%G" /E
)
