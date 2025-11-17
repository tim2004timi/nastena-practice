import 'dart:io';
import 'package:image/image.dart' as img;

void main() async {
  print('Создание иконки приложения...');
  
  // Создаем изображение 1024x1024
  final image = img.Image(width: 1024, height: 1024);
  
  // Заполняем фиолетовым фоном (#9D4EDD)
  final backgroundColor = img.ColorRgb8(157, 78, 221); // #9D4EDD
  img.fill(image, color: backgroundColor);
  
  // Создаем простую иконку шапочки (упрощенная версия)
  // В реальности лучше использовать готовое изображение
  final iconColor = img.ColorRgb8(255, 255, 255);
  
  // Рисуем простую шапочку (упрощенная версия)
  // Это очень простая версия, лучше использовать готовое изображение
  final centerX = 512;
  final centerY = 400;
  
  // Основание шапочки (квадрат)
  img.fillRect(image, 
    x1: centerX - 200, 
    y1: centerY - 50, 
    x2: centerX + 200, 
    y2: centerY + 50, 
    color: iconColor);
  
  // Кисточка
  img.drawLine(image, 
    x1: centerX + 200, 
    y1: centerY, 
    x2: centerX + 250, 
    y2: centerY + 100, 
    color: iconColor, 
    thickness: 20);
  
  // Сохраняем основную иконку
  final iconFile = File('assets/icon/app_icon.png');
  await iconFile.parent.create(recursive: true);
  await iconFile.writeAsBytes(img.encodePng(image));
  print('Создана основная иконка: ${iconFile.path}');
  
  // Создаем foreground версию (только иконка на прозрачном фоне)
  final foreground = img.Image(width: 1024, height: 1024);
  // Прозрачный фон (изображение уже прозрачное по умолчанию)
  
  // Рисуем ту же иконку
  img.fillRect(foreground, 
    x1: centerX - 200, 
    y1: centerY - 50, 
    x2: centerX + 200, 
    y2: centerY + 50, 
    color: iconColor);
  
  img.drawLine(foreground, 
    x1: centerX + 200, 
    y1: centerY, 
    x2: centerX + 250, 
    y2: centerY + 100, 
    color: iconColor, 
    thickness: 20);
  
  final foregroundFile = File('assets/icon/app_icon_foreground.png');
  await foregroundFile.writeAsBytes(img.encodePng(foreground));
  print('Создана foreground иконка: ${foregroundFile.path}');
  
  print('\n⚠️  ВНИМАНИЕ: Это упрощенная версия иконки!');
  print('Для лучшего качества рекомендуется:');
  print('1. Использовать готовое изображение шапочки выпускника');
  print('2. Или создать иконку в графическом редакторе');
  print('3. Сохранить как assets/icon/app_icon.png и app_icon_foreground.png');
  print('\nПосле создания иконок запустите:');
  print('flutter pub run flutter_launcher_icons');
}

