{{- define "cloudforge.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- define "cloudforge.fullname" -}}
{{- printf "%s" (include "cloudforge.name" .) | trunc 63 | trimSuffix "-" -}}
{{- end -}}
