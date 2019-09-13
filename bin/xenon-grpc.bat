@rem
@rem Copyright 2015 the original author or authors.
@rem
@rem Licensed under the Apache License, Version 2.0 (the "License");
@rem you may not use this file except in compliance with the License.
@rem You may obtain a copy of the License at
@rem
@rem      http://www.apache.org/licenses/LICENSE-2.0
@rem
@rem Unless required by applicable law or agreed to in writing, software
@rem distributed under the License is distributed on an "AS IS" BASIS,
@rem WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@rem See the License for the specific language governing permissions and
@rem limitations under the License.
@rem

@if "%DEBUG%" == "" @echo off
@rem ##########################################################################
@rem
@rem  xenon-grpc startup script for Windows
@rem
@rem ##########################################################################

@rem Set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" setlocal

set DIRNAME=%~dp0
if "%DIRNAME%" == "" set DIRNAME=.
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%..

@rem Add default JVM options here. You can also use JAVA_OPTS and XENON_GRPC_OPTS to pass JVM options to this script.
set DEFAULT_JVM_OPTS=

@rem Find java.exe
if defined JAVA_HOME goto findJavaFromJavaHome

set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if "%ERRORLEVEL%" == "0" goto init

echo.
echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe

if exist "%JAVA_EXE%" goto init

echo.
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:init
@rem Get command-line arguments, handling Windows variants

if not "%OS%" == "Windows_NT" goto win9xME_args

:win9xME_args
@rem Slurp the command line arguments.
set CMD_LINE_ARGS=
set _SKIP=2

:win9xME_args_slurp
if "x%~1" == "x" goto execute

set CMD_LINE_ARGS=%*

:execute
@rem Setup the command line

set CLASSPATH=%APP_HOME%\lib\xenon-grpc-3.0.1.jar;%APP_HOME%\lib\grpc-netty-1.21.0.jar;%APP_HOME%\lib\grpc-services-1.21.0.jar;%APP_HOME%\lib\grpc-protobuf-1.21.0.jar;%APP_HOME%\lib\grpc-stub-1.21.0.jar;%APP_HOME%\lib\xenon-adaptors-cloud-3.0.2.jar;%APP_HOME%\lib\xenon-3.0.4.jar;%APP_HOME%\lib\logback-classic-1.0.11.jar;%APP_HOME%\lib\sshd-mina-2.2.0.jar;%APP_HOME%\lib\mina-core-2.0.19.jar;%APP_HOME%\lib\sshd-sftp-2.2.0.jar;%APP_HOME%\lib\sshd-core-2.2.0.jar;%APP_HOME%\lib\sshd-common-2.2.0.jar;%APP_HOME%\lib\slf4j-api-1.7.25.jar;%APP_HOME%\lib\argparse4j-0.8.1.jar;%APP_HOME%\lib\netty-tcnative-boringssl-static-2.0.25.Final.jar;%APP_HOME%\lib\grpc-core-1.21.0.jar;%APP_HOME%\lib\netty-codec-http2-4.1.34.Final.jar;%APP_HOME%\lib\netty-handler-proxy-4.1.34.Final.jar;%APP_HOME%\lib\grpc-protobuf-lite-1.21.0.jar;%APP_HOME%\lib\grpc-api-1.21.0.jar;%APP_HOME%\lib\protobuf-java-util-3.7.1.jar;%APP_HOME%\lib\protobuf-java-3.7.1.jar;%APP_HOME%\lib\aws-s3-2.1.2.jar;%APP_HOME%\lib\s3-2.1.2.jar;%APP_HOME%\lib\sts-2.1.2.jar;%APP_HOME%\lib\jclouds-blobstore-2.1.2.jar;%APP_HOME%\lib\jclouds-core-2.1.2.jar;%APP_HOME%\lib\guava-26.0-android.jar;%APP_HOME%\lib\proto-google-common-protos-1.12.0.jar;%APP_HOME%\lib\logback-core-1.0.11.jar;%APP_HOME%\lib\commons-net-3.3.jar;%APP_HOME%\lib\eddsa-0.3.0.jar;%APP_HOME%\lib\jaxb-api-2.3.1.jar;%APP_HOME%\lib\jaxb-core-2.3.0.1.jar;%APP_HOME%\lib\jaxb-impl-2.3.1.jar;%APP_HOME%\lib\activation-1.1.1.jar;%APP_HOME%\lib\sardine-5.8.jar;%APP_HOME%\lib\opencensus-contrib-grpc-metrics-0.21.0.jar;%APP_HOME%\lib\opencensus-api-0.21.0.jar;%APP_HOME%\lib\gson-2.7.jar;%APP_HOME%\lib\annotations-4.1.1.4.jar;%APP_HOME%\lib\netty-codec-http-4.1.34.Final.jar;%APP_HOME%\lib\netty-handler-4.1.34.Final.jar;%APP_HOME%\lib\netty-codec-socks-4.1.34.Final.jar;%APP_HOME%\lib\netty-codec-4.1.34.Final.jar;%APP_HOME%\lib\netty-transport-4.1.34.Final.jar;%APP_HOME%\lib\netty-buffer-4.1.34.Final.jar;%APP_HOME%\lib\netty-resolver-4.1.34.Final.jar;%APP_HOME%\lib\netty-common-4.1.34.Final.jar;%APP_HOME%\lib\grpc-context-1.21.0.jar;%APP_HOME%\lib\error_prone_annotations-2.3.2.jar;%APP_HOME%\lib\jsr305-3.0.2.jar;%APP_HOME%\lib\animal-sniffer-annotations-1.17.jar;%APP_HOME%\lib\checker-compat-qual-2.5.2.jar;%APP_HOME%\lib\j2objc-annotations-1.1.jar;%APP_HOME%\lib\javax.activation-api-1.2.0.jar;%APP_HOME%\lib\httpclient-4.5.1.jar;%APP_HOME%\lib\java-xmlbuilder-1.1.jar;%APP_HOME%\lib\httpcore-4.4.3.jar;%APP_HOME%\lib\commons-logging-1.2.jar;%APP_HOME%\lib\commons-codec-1.9.jar;%APP_HOME%\lib\base64-2.3.8.jar;%APP_HOME%\lib\javax.ws.rs-api-2.0.1.jar;%APP_HOME%\lib\guice-assistedinject-3.0.jar;%APP_HOME%\lib\guice-3.0.jar;%APP_HOME%\lib\javax.inject-1.jar;%APP_HOME%\lib\jsr250-api-1.0.jar;%APP_HOME%\lib\aopalliance-1.0.jar;%APP_HOME%\lib\cglib-2.2.1-v20090111.jar;%APP_HOME%\lib\asm-3.1.jar

@rem Execute xenon-grpc
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %XENON_GRPC_OPTS%  -classpath "%CLASSPATH%" nl.esciencecenter.xenon.grpc.XenonServerWrapper %CMD_LINE_ARGS%

:end
@rem End local scope for the variables with windows NT shell
if "%ERRORLEVEL%"=="0" goto mainEnd

:fail
rem Set variable XENON_GRPC_EXIT_CONSOLE if you need the _script_ return code instead of
rem the _cmd.exe /c_ return code!
if  not "" == "%XENON_GRPC_EXIT_CONSOLE%" exit 1
exit /b 1

:mainEnd
if "%OS%"=="Windows_NT" endlocal

:omega
