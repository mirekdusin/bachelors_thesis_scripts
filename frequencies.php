<?php

$file = fopen("binary.csv", "r");

$all_comb = array();

while (!feof($file)) {
    $line = fgets($file);
    $line = preg_replace("/\r|\n/", "", $line);
    array_push($all_comb, $line);
}

$all_keywords = array_count_values($all_comb);
arsort($all_keywords);
print_r($all_keywords);
