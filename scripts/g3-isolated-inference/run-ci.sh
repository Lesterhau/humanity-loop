#!/usr/bin/env bash
set -euo pipefail
set +x
umask 077
[[ "${GITHUB_ACTIONS:-}" == true && "${CI:-}" == true && "${HL_APPROVED_ONE_SHOT:-}" == true && "${GITHUB_REPOSITORY:-}" == Lesterhau/humanity-loop && "${GITHUB_EVENT_NAME:-}" == pull_request && "${GITHUB_HEAD_REF:-}" == test/g3-isolated-inference-20261124 && "${GITHUB_RUN_ATTEMPT:-}" == 1 ]] || exit 2
here=$(cd -- "$(dirname -- "$0")" && pwd)
root=$(git -C "$here" rev-parse --show-toplevel)
work=$(mktemp -d)
cid=''
cleanup(){ if [[ -n "$cid" ]]; then docker rm -f "$cid" >/dev/null 2>&1 || true; fi; rm -rf -- "$work"; }
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
image='ghcr.io/ggml-org/llama.cpp:server-b9519@sha256:abaf7899e16b638411096f6db42563dffa876119037458b7986f2a6bde3df41e'
url='https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B-Instruct-GGUF/resolve/2d4a76a30b4af41ecd395c35725ac11688d4cfe4/smollm2-1.7b-instruct-q4_k_m.gguf'
expected='decd2598bc2c8ed08c19adc3c8fdd461ee19ed5708679d1c54ef54a5a30d4f33'
curl -q --fail --silent --show-error --location --proto '=https' --proto-redir '=https' --max-redirs 5 --max-time 180 --max-filesize 1200000000 "$url" -o "$work/model.gguf"
printf '%s  %s\n' "$expected" "$work/model.gguf" | sha256sum -c -
chmod 0444 "$work/model.gguf"
docker pull --platform linux/amd64 "$image"
cid=$(docker run -d --pull never --platform linux/amd64 --network none --cap-drop ALL --security-opt no-new-privileges --read-only --tmpfs /tmp:rw,noexec,nosuid,size=128m --user 65534:65534 --memory 6g --cpus 4 --pids-limit 128 --mount "type=bind,src=$work/model.gguf,dst=/model.gguf,readonly" "$image" --model /model.gguf --alias hl-pinned-smollm2 --host 127.0.0.1 --port 8080 --ctx-size 4096 --parallel 1 --threads 4 --n-gpu-layers 0 --n-predict 256)
[[ $(docker inspect -f '{{.HostConfig.NetworkMode}}' "$cid") == none ]] || exit 2
[[ $(docker inspect -f '{{.HostConfig.Privileged}}' "$cid") == false ]] || exit 2
pid=$(docker inspect -f '{{.State.Pid}}' "$cid")
[[ "$pid" =~ ^[1-9][0-9]*$ ]] || exit 2
[[ $(readlink /proc/self/ns/net) != $(sudo readlink "/proc/$pid/ns/net") ]] || exit 2
user=$(id -un)
ready=0
for i in $(seq 1 90); do
 if sudo nsenter -t "$pid" -n -- curl -q --noproxy '*' --max-time 1 --fail --silent http://127.0.0.1:8080/health >/dev/null; then ready=1; break; fi
 sleep 1
done
[[ "$ready" == 1 ]] || { echo 'Model readiness not established; no inference authorized'; exit 2; }
# Independent wall-clock watchdog supplements the adapter's deadline.
sudo timeout --kill-after=5s 240s nsenter -t "$pid" -n -- sudo -u "$user" env -i PATH=/usr/bin:/bin HL_APPROVED_ONE_SHOT=true /usr/bin/python3 "$here/run_fixture.py" "$root" "$work/receipt.json"
sha256sum "$work/receipt.json" | cut -d' ' -f1
