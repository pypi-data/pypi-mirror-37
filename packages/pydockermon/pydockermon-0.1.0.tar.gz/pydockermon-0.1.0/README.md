# pydockermon [![Build Status](https://travis-ci.com/ludeeus/pydockermon.svg?branch=master)](https://travis-ci.com/ludeeus/pydockermon) [![PyPI version](https://badge.fury.io/py/pydockermon.svg)](https://badge.fury.io/py/pydockermon)

_A python module to interact with ha-dockermon._

## Install

```bash
pip install pydockermon
```

## Usage

```python
import pydockermon

host = '192.168.1.3'
container = 'MyFirstContainer'

print(pydockermon.list_containers(host))
> {'data': ['MyFirstContainer', 'MySecondContainer'], 'success': True}

print(pydockermon.get_container_state(container, host))
> {'data': {'status': 'Up 2 minutes', 'image': 'homeassistant/home-assistant', 'state': 'running'}, 'success': True}

print(pydockermon.get_container_stats(container, host))
> {'data': {'blkio_stats': {'io_time_recursive': [{'minor': 0, 'value': 930522371, 'major': 8, 'op': ''}], 'io_service_time_recursive': [{'minor': 0, 'value': 101697738, 'major': 8, 'op': 'Read'}, {'minor': 0, 'value': 449528677, 'major': 8, 'op': 'Write'}, {'minor': 0, 'value': 413017572, 'major': 8, 'op': 'Sync'}, {'minor': 0, 'value': 138208843, 'major': 8, 'op': 'Async'}, {'minor': 0, 'value': 551226415, 'major': 8, 'op': 'Total'}], 'io_queue_recursive': [{'minor': 0, 'value': 0, 'major': 8, 'op': 'Read'}, {'minor': 0, 'value': 0, 'major': 8, 'op': 'Write'}, {'minor': 0, 'value': 0, 'major': 8, 'op': 'Sync'}, {'minor': 0, 'value': 0, 'major': 8, 'op': 'Async'}, {'minor': 0, 'value': 0, 'major': 8, 'op': 'Total'}], 'sectors_recursive': [{'minor': 0, 'value': 12040, 'major': 8, 'op': ''}], 'io_merged_recursive': [{'minor': 0, 'value': 0, 'major': 8, 'op': 'Read'}, {'minor': 0, 'value': 0, 'major': 8, 'op': 'Write'}, {'minor': 0, 'value': 0, 'major': 8, 'op': 'Sync'}, {'minor': 0, 'value': 0, 'major': 8, 'op': 'Async'}, {'minor': 0, 'value': 0, 'major': 8, 'op': 'Total'}], 'io_service_bytes_recursive': [{'minor': 0, 'value': 20480, 'major': 8, 'op': 'Read'}, {'minor': 0, 'value': 6144000, 'major': 8, 'op': 'Write'}, {'minor': 0, 'value': 3981312, 'major': 8, 'op': 'Sync'}, {'minor': 0, 'value': 2183168, 'major': 8, 'op': 'Async'}, {'minor': 0, 'value': 6164480, 'major': 8, 'op': 'Total'}, {'minor': 0, 'value': 20480, 'major': 8, 'op': 'Read'}, {'minor': 0, 'value': 6144000, 'major': 8, 'op': 'Write'}, {'minor': 0, 'value': 3981312, 'major': 8, 'op': 'Sync'}, {'minor': 0, 'value': 2183168, 'major': 8, 'op': 'Async'}, {'minor': 0, 'value': 6164480, 'major': 8, 'op': 'Total'}], 'io_serviced_recursive': [{'minor': 0, 'value': 5, 'major': 8, 'op': 'Read'}, {'minor': 0, 'value': 595, 'major': 8, 'op': 'Write'}, {'minor': 0, 'value': 529, 'major': 8, 'op': 'Sync'}, {'minor': 0, 'value': 71, 'major': 8, 'op': 'Async'}, {'minor': 0, 'value': 600, 'major': 8, 'op': 'Total'}, {'minor': 0, 'value': 5, 'major': 8, 'op': 'Read'}, {'minor': 0, 'value': 595, 'major': 8, 'op': 'Write'}, {'minor': 0, 'value': 529, 'major': 8, 'op': 'Sync'}, {'minor': 0, 'value': 71, 'major': 8, 'op': 'Async'}, {'minor': 0, 'value': 600, 'major': 8, 'op': 'Total'}], 'io_wait_time_recursive': [{'minor': 0, 'value': 102969, 'major': 8, 'op': 'Read'}, {'minor': 0, 'value': 3944505179, 'major': 8, 'op': 'Write'}, {'minor': 0, 'value': 3454882493, 'major': 8, 'op': 'Sync'}, {'minor': 0, 'value': 489725655, 'major': 8, 'op': 'Async'}, {'minor': 0, 'value': 3944608148, 'major': 8, 'op': 'Total'}]}, 'cpu_stats': {'online_cpus': 2, 'system_cpu_usage': 618664310000000, 'cpu_usage': {'percpu_usage': [2553071243, 950276267], 'usage_in_usermode': 2930000000, 'usage_in_kernelmode': 540000000, 'total_usage': 3503347510}, 'throttling_data': {'throttled_time': 0, 'throttled_periods': 0, 'periods': 0}}, 'name': '/homeassistanttest', 'storage_stats': {}, 'preread': '2018-10-28T08:56:34.970419252Z', 'num_procs': 0, 'id': '3a45c882e9aedbb38e15bd91764d769329497a3abbc26e6b220f5ca9c122ec01', 'memory_stats': {'max_usage': 67948544, 'usage': 66768896, 'limit': 4047405056, 'stats': {'total_rss': 65294336, 'pgfault': 38626, 'total_mapped_file': 0, 'pgpgin': 20015, 'total_active_file': 16384, 'cache': 49152, 'total_rss_huge': 0, 'active_anon': 65294336, 'mapped_file': 0, 'total_pgpgout': 4062, 'total_pgpgin': 20015, 'rss': 65294336, 'pgmajfault': 0, 'total_unevictable': 0, 'hierarchical_memory_limit': 9223372036854772000, 'pgpgout': 4062, 'writeback': 0, 'active_file': 16384, 'total_cache': 49152, 'inactive_file': 32768, 'dirty': 0, 'inactive_anon': 0, 'rss_huge': 0, 'hierarchical_memsw_limit': 0, 'total_writeback': 0, 'total_pgfault': 38626, 'total_inactive_anon': 0, 'unevictable': 0, 'total_dirty': 0, 'total_inactive_file': 32768, 'total_active_anon': 65294336, 'total_pgmajfault': 0}}, 'networks': {'eth0': {'tx_bytes': 13916, 'rx_packets': 47, 'tx_errors': 0, 'rx_errors': 0, 'tx_packets': 151, 'tx_dropped': 0, 'rx_bytes': 29783, 'rx_dropped': 0}}, 'pids_stats': {'current': 17}, 'read': '2018-10-28T08:56:35.972372723Z', 'precpu_stats': {'online_cpus': 2, 'system_cpu_usage': 618662320000000, 'cpu_usage': {'percpu_usage': [2553071243, 949852666], 'usage_in_usermode': 2930000000, 'usage_in_kernelmode': 540000000, 'total_usage': 3502923909}, 'throttling_data': {'throttled_time': 0, 'throttled_periods': 0, 'periods': 0}}}, 'success': True}

print(pydockermon.stop_container(container, host))
> {'data': {}, 'success': True}

print(pydockermon.start_container(container, host))
> {'data': {}, 'success': True}

print(pydockermon.restart_container(container, host))
> {'data': {}, 'success': True}

```