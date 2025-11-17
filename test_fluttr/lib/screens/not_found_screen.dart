import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../utils/colors.dart';
import '../utils/gradients.dart';

class NotFoundScreen extends StatelessWidget {
  const NotFoundScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(gradient: AppGradients.backgroundGradient),
        child: SafeArea(
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  '404',
                  style: TextStyle(
                    color: AppColors.foreground,
                    fontSize: 48,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  'Oops! Page not found',
                  style: TextStyle(
                    color: AppColors.mutedForeground,
                    fontSize: 20,
                  ),
                ),
                const SizedBox(height: 32),
                GestureDetector(
                  onTap: () => context.go('/'),
                  child: Text(
                    'Return to Home',
                    style: TextStyle(
                      color: AppColors.primary,
                      fontSize: 16,
                      decoration: TextDecoration.underline,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

