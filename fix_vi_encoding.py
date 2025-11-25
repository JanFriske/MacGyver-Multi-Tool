import json
import os

vi_data = {
    "menu": {
        "file": "Tệp",
        "edit": "Chỉnh sửa",
        "view": "Xem",
        "tools": "Công cụ",
        "settings": "Cài đặt",
        "help": "Trợ giúp",
        "languages": "Ngôn ngữ",
        "german_dialects": "Tiếng Đức"
    },
    "menu_file": {
        "new": "Mới",
        "open": "Mở...",
        "save": "Lưu",
        "exit": "Thoát"
    },
    "menu_edit": {
        "undo": "Hoàn tác",
        "redo": "Làm lại"
    },
    "menu_view": {
        "theme_light": "Giao diện Sáng",
        "theme_dark": "Giao diện Tối"
    },
    "menu_tools": {
        "cockpit": "Buồng lái",
        "media": "Phương tiện",
        "tabs": "Thẻ",
        "add_widget": "➕ Thêm Widget...",
        "system_monitor": "Giám sát hệ thống",
        "clock": "Đồng hồ thế giới",
        "network_traffic": "Lưu lượng mạng",
        "gpu_monitor": "Giám sát GPU",
        "temperature": "Nhiệt độ",
        "disk_io": "Đĩa I/O",
        "media_controls": "Điều khiển phương tiện",
        "video_screen": "Màn hình Video",
        "media_explorer": "Trình duyệt phương tiện",
        "stream": "Luồng trực tuyến",
        "equalizer": "Bộ cân bằng",
        "file_manager": "Quản lý tệp",
        "network_diag": "Chẩn đoán mạng"
    },
    "widgets": {
        "clock": "Đồng hồ thế giới",
        "system_monitor": "Giám sát hệ thống",
        "network_monitor": "Lưu lượng mạng",
        "gpu_monitor": "Giám sát GPU",
        "temp_monitor": "Nhiệt độ",
        "disk_io_monitor": "Đĩa I/O",
        "directory_browser": "Quản lý tệp",
        "quick_access": "Truy cập nhanh",
        "file_stats": "Thống kê",
        "recent_files": "Tệp gần đây",
        "ping": "Ping",
        "connection_status": "Kết nối",
        "speed_test": "Kiểm tra tốc độ",
        "active_connections": "Kết nối hoạt động",
        "network_path": "Đường dẫn mạng",
        "directory_browser_title": "Quản lý tệp",
        "quick_access_title": "Truy cập nhanh",
        "file_stats_title": "Thống kê",
        "file_stats_storage": "Lưu trữ",
        "recent_files_title": "Tệp gần đây"
    },
    "dialogs": {
        "about": {
            "title": "Về MacGyver Multi-Tool",
            "version": "Phiên bản 1.0 (Bản dựng MVP)",
            "description": "Một công cụ tiện ích mô-đun với thiết kế macOS.",
            "copyright": "© 2025 Jan Friske – Đã đăng ký bản quyền.",
            "license": "Giấy phép miễn phí (phi thương mại)."
        },
        "widget_selector": {
            "title": "Thêm Widget",
            "preview": "Xem trước",
            "size_select": "Chọn kích thước:",
            "add_button": "Thêm vào Bảng điều khiển",
            "sizes": {
                "compact": "Nhỏ gọn",
                "wide": "Rộng",
                "extra_wide": "Rất rộng",
                "full_width": "Toàn chiều rộng",
                "tall": "Cao",
                "large": "Lớn",
                "extra_large": "Rất lớn",
                "maximum": "Tối đa"
            },
            "scale": "Tỷ lệ",
            "error": "Lỗi xem trước"
        }
    },
    "tabs": {
        "cockpit": "Buồng lái",
        "media_commander": "Chỉ huy phương tiện"
    },
    "weather": {
        "loading": "Đang tải...",
        "loading_data": "Đang tải dữ liệu thời tiết...",
        "forecast": "Dự báo 3 ngày",
        "feels_like": "Cảm giác như",
        "humidity": "Độ ẩm",
        "wind": "Gió",
        "unknown": "Không rõ"
    },
    "time": {
        "zone": "Múi giờ",
        "calendar_week": "Tuần lịch",
        "day_of_year": "Ngày trong năm",
        "day_of_year_full": "Ngày thứ {day} trong năm",
        "summer_time": "Giờ mùa hè",
        "winter_time": "Giờ mùa đông",
        "gmt_offset": "GMT: {time} ({offset})",
        "timezone_label": "Múi giờ: {name}",
        "week_day": "Tuần {week} • Ngày {day}"
    },
    "gauges": {
        "cpu": "CPU",
        "ram": "RAM",
        "upload": "Tải lên",
        "download": "Tải xuống",
        "gpu": "GPU",
        "system": "Hệ thống"
    },
    "disk_io": {
        "disk_label": "Đĩa: {name}",
        "read": "Đ",
        "write": "G"
    },
    "file_manager": {
        "up": "⬆️ Lên",
        "folders": "Thư mục",
        "files": "Tệp",
        "headers": {
            "name": "Tên",
            "size": "Kích thước",
            "modified": "Đã sửa đổi"
        },
        "places": {
            "desktop": "Màn hình chính",
            "documents": "Tài liệu",
            "downloads": "Tải xuống",
            "pictures": "Hình ảnh",
            "music": "Nhạc",
            "videos": "Video",
            "home": "Trang chủ"
        },
        "stats": {
            "files_count": "{count} tệp",
            "storage": "Lưu trữ"
        },
        "up_button": "⬆️ Lên"
    },
    "network": {
        "ping": {
            "btn": "🌐 Ping",
            "placeholder": "Tên máy chủ hoặc IP",
            "pinging": "Đang ping {host}...",
            "failed": "❌ Ping thất bại",
            "timeout": "❌ Hết thời gian"
        },
        "connection": {
            "checking": "Đang kiểm tra...",
            "connected": "Đã kết nối",
            "disconnected": "Đã ngắt kết nối",
            "no_connection": "Không có kết nối",
            "ip_label": "IP: {ip}"
        },
        "speed_test": {
            "btn": "🚀 Kiểm tra tốc độ",
            "testing": "Đang kiểm tra...",
            "download": "Tải xuống",
            "upload": "Tải lên"
        },
        "active_connections": {
            "protocol": "Giao thức",
            "refresh": "🔄 Làm mới",
            "all": "Tất cả",
            "headers": {
                "process": "Tiến trình",
                "protocol": "Giao thức",
                "local": "Cục bộ",
                "remote": "Từ xa",
                "status": "Trạng thái"
            }
        },
        "trace": {
            "target": "Mục tiêu:",
            "btn": "🗺️ Truy vết đường đi",
            "placeholder": "Tên máy chủ hoặc IP",
            "tracing": "Đang truy vết...",
            "start_msg": "🗺️ Đường đi đến mục tiêu sẽ hiển thị ở đây.\nNhập mục tiêu và nhấp vào 'Truy vết đường đi'.",
            "loading": "⏳ Đang xác định đường đi...",
            "you": "🖥️ Bạn",
            "destination": "🎯 Đích",
            "timeout": "Hết thời gian: Không thể xác định đường đi đầy đủ.",
            "error": "Lỗi: {error}",
            "no_route": "Không tìm thấy đường đi hoặc lỗi truy vết."
        }
    },
    "units": {
        "celsius": "°C",
        "percent": "%",
        "mbps": "Mbps",
        "kbps": "KB/s",
        "ms": "ms",
        "bytes": "B",
        "kilobytes": "KB",
        "megabytes": "MB",
        "gigabytes": "GB",
        "terabytes": "TB"
    },
    "status": {
        "loading": "Đang tải...",
        "error": "Lỗi",
        "unknown": "Không rõ",
        "timeout": "Hết thời gian",
        "local": "Cục bộ",
        "checking": "Đang kiểm tra..."
    },
    "media": {
        "open_button": "Mở",
        "equalizer_preset_label": "Cài đặt sẵn:",
        "equalizer_presets": {
            "flat": "Phẳng",
            "rock": "Rock",
            "pop": "Pop",
            "jazz": "Jazz",
            "classical": "Cổ điển",
            "bass_boost": "Tăng cường Bass"
        }
    }
}

output_path = "c:/Dev/Repos/JanFriske/MacGyver Multi-Tool/i18n/translations/vi.json"
with open(output_path, 'w', encoding='utf-8') as f:
    # ensure_ascii=True will escape all non-ASCII characters (e.g. \u1234)
    # This ensures the file is safe for any encoding
    json.dump(vi_data, f, indent=4, ensure_ascii=True)

print(f"Regenerated {output_path} with escaped unicode.")
