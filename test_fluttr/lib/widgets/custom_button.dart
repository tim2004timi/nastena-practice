import 'package:flutter/material.dart';
import '../utils/colors.dart';

enum ButtonVariant { default_, outline, ghost, destructive }
enum ButtonSize { default_, sm, lg, icon }

class CustomButton extends StatelessWidget {
  final String? label;
  final IconData? icon;
  final VoidCallback? onPressed;
  final ButtonVariant variant;
  final ButtonSize size;
  final bool isFullWidth;

  const CustomButton({
    super.key,
    this.label,
    this.icon,
    this.onPressed,
    this.variant = ButtonVariant.default_,
    this.size = ButtonSize.default_,
    this.isFullWidth = false,
  }) : assert(label != null || icon != null, 'Either label or icon must be provided');

  @override
  Widget build(BuildContext context) {
    final height = _getHeight();
    final width = isFullWidth ? double.infinity : (size == ButtonSize.icon ? height : null);

    Widget child;
    if (icon != null && label != null) {
      child = Row(
        mainAxisSize: MainAxisSize.min,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, size: 20),
          const SizedBox(width: 8),
          Text(label!),
        ],
      );
    } else if (icon != null) {
      child = Icon(icon, size: 20);
    } else {
      child = Text(label!);
    }

    final button = _buildButton(child, height, width);

    if (onPressed == null) {
      return Opacity(
        opacity: 0.5,
        child: button,
      );
    }

    return GestureDetector(
      onTap: onPressed,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 150),
        curve: Curves.easeInOut,
        child: button,
      ),
    );
  }

  Widget _buildButton(Widget child, double height, double? width) {
    Color backgroundColor;
    Color textColor;
    Color? borderColor;
    double? borderWidth;

    switch (variant) {
      case ButtonVariant.default_:
        backgroundColor = AppColors.primary;
        textColor = Colors.white;
        borderColor = null;
        borderWidth = null;
        break;
      case ButtonVariant.outline:
        backgroundColor = Colors.transparent;
        textColor = AppColors.foreground;
        borderColor = AppColors.input;
        borderWidth = 1;
        break;
      case ButtonVariant.ghost:
        backgroundColor = Colors.transparent;
        textColor = AppColors.foreground;
        borderColor = null;
        borderWidth = null;
        break;
      case ButtonVariant.destructive:
        backgroundColor = AppColors.destructive;
        textColor = Colors.white;
        borderColor = null;
        borderWidth = null;
        break;
    }

    return Container(
      width: width,
      height: height,
      constraints: BoxConstraints(
        minHeight: 48, // touch-target
        minWidth: size == ButtonSize.icon ? 48 : 0,
      ),
      decoration: BoxDecoration(
        color: backgroundColor,
        border: borderColor != null ? Border.all(color: borderColor, width: borderWidth!) : null,
        borderRadius: BorderRadius.circular(6),
      ),
      child: Center(
        child: Padding(
          padding: EdgeInsets.symmetric(
            horizontal: size == ButtonSize.icon ? 0 : (size == ButtonSize.sm ? 12 : 16),
            vertical: size == ButtonSize.icon ? 0 : 8,
          ),
          child: DefaultTextStyle(
            style: TextStyle(
              color: textColor,
              fontSize: size == ButtonSize.sm ? 14 : 16,
              fontWeight: FontWeight.w500,
            ),
            child: child,
          ),
        ),
      ),
    );
  }

  double _getHeight() {
    switch (size) {
      case ButtonSize.sm:
        return 36;
      case ButtonSize.default_:
        return 40;
      case ButtonSize.lg:
        return 44;
      case ButtonSize.icon:
        return 40;
    }
  }
}

