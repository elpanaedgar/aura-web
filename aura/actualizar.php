<?php
/* AURĀ · Sincroniza esta carpeta con GitHub (elpanaedgar/aura-web, carpeta aura/).
   GitHub llama a esta página después de cada cambio: ?sha=<commit>.
   Solo descarga los archivos de la lista archivos.txt de ese commit; no acepta otras rutas ni otro repositorio. */
header('Content-Type: text/plain; charset=utf-8');
header('Cache-Control: no-store');
$repo = 'elpanaedgar/aura-web';
$sha = isset($_GET['sha']) ? $_GET['sha'] : 'main';
if (!preg_match('/^([0-9a-f]{40}|main)$/', $sha)) { http_response_code(400); exit("Versión no válida\n"); }
$lock = __DIR__ . '/.aura-ultima-actualizacion';
if (file_exists($lock) && time() - filemtime($lock) < 15) { http_response_code(429); exit("Espera unos segundos y vuelve a intentarlo\n"); }
@touch($lock);
$base = 'https://raw.githubusercontent.com/' . $repo . '/' . $sha . '/aura/';

function aura_get($url) {
  if (function_exists('curl_init')) {
    $c = curl_init($url);
    curl_setopt_array($c, array(CURLOPT_RETURNTRANSFER => true, CURLOPT_FOLLOWLOCATION => true, CURLOPT_TIMEOUT => 60, CURLOPT_USERAGENT => 'AURA-sync'));
    $b = curl_exec($c); $code = curl_getinfo($c, CURLINFO_HTTP_CODE); curl_close($c);
    return ($code === 200) ? $b : false;
  }
  $ctx = stream_context_create(array('http' => array('timeout' => 60, 'header' => "User-Agent: AURA-sync\r\n")));
  return @file_get_contents($url, false, $ctx);
}

$list = aura_get($base . 'archivos.txt');
if ($list === false) { http_response_code(502); exit("No se pudo leer la lista de archivos desde GitHub\n"); }
$ok = 0; $fail = array();
foreach (preg_split('/\r?\n/', trim($list)) as $rel) {
  $rel = trim($rel);
  if ($rel === '' || $rel === 'actualizar.php') continue;
  if (!preg_match('#^[A-Za-z0-9_\-]+(/[A-Za-z0-9_\-]+)*\.[A-Za-z0-9]+$#', $rel)) { $fail[] = $rel . ' (ruta no permitida)'; continue; }
  $data = aura_get($base . $rel);
  if ($data === false) { $fail[] = $rel; continue; }
  $dest = __DIR__ . '/' . $rel;
  if (!is_dir(dirname($dest))) @mkdir(dirname($dest), 0755, true);
  $tmp = $dest . '.tmp-aura';
  if (@file_put_contents($tmp, $data) === false || !@rename($tmp, $dest)) { @unlink($tmp); $fail[] = $rel . ' (sin permiso de escritura)'; continue; }
  $ok++;
}
if ($fail) { http_response_code(500); echo "Actualizados: $ok\nFallos:\n- " . implode("\n- ", $fail) . "\n"; exit; }
echo "OK · $ok archivos actualizados desde " . substr($sha, 0, 7) . "\n";
