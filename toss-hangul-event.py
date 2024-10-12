import pytesseract
from PIL import Image, ImageDraw
import pyautogui
import os

# Tesseract 경로 설정 (실제 설치된 경로로 수정)
pytesseract.pytesseract.tesseract_cmd = '/opt/local/bin/tesseract'  # Tesseract 설치 경로

# OCR로 이미지를 분석해 한글 단어를 인식하고 해당 위치를 찾는 함수
def extract_text_with_position(image_path):
    image = Image.open(image_path)
    
    # psm 설정을 추가하여 단어를 좀 더 정확하게 인식
    custom_config = r'--oem 3 --psm 6'  # psm 6: 단어 블록 단위로 분석
    
    data = pytesseract.image_to_data(image, lang='kor', output_type=pytesseract.Output.DICT, config=custom_config)
    words = data['text']  # OCR로 인식된 단어들
    positions = []  # 단어 위치를 저장할 리스트

    # 단어들과 그 위치 정보를 추출
    for i, word in enumerate(words):
        if word.strip():  # 빈 단어가 아닌 경우
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            positions.append((word, (x, y, w, h)))
    
    return positions

# 다른 단어를 찾아내는 함수
def find_different_word_with_position(positions):
    word_counts = {}
    
    # 단어 빈도 계산
    for word, position in positions:
        word_counts[word] = word_counts.get(word, 0) + 1
    
    # 가장 적게 나온 단어를 찾음
    for word, position in positions:
        if word_counts[word] == 1:
            return word, position
    return None, None

# 스크린샷 좌표를 실제 화면 좌표로 변환하는 함수
def convert_image_coords_to_screen(image_coords, screen_offset):
    x, y, w, h = image_coords
    screen_x_offset, screen_y_offset = screen_offset

    # 좌표 변환 (스크린샷 좌표에 스크린샷 시작 좌표를 더해 실제 화면 좌표로 변환)
    screen_x = x + screen_x_offset
    screen_y = y + screen_y_offset

    return screen_x, screen_y

# 화면에서 특정 영역을 캡쳐하는 함수
def capture_screenshot(x_start, y_start, width, height, save_path):
    # 스크린샷을 찍을 디렉토리가 없으면 생성
    save_dir = os.path.dirname(save_path)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"폴더 생성 완료: {save_dir}")
    
    screenshot = pyautogui.screenshot(region=(x_start, y_start, width, height))
    screenshot.save(save_path)
    print(f"스크린샷 저장 완료: {save_path}")

# 메인 실행 함수
def solve_quiz(x_start, y_start, width, height, image_path, screen_offset):
    # 화면에서 퀴즈 부분 캡쳐
    capture_screenshot(x_start, y_start, width, height, image_path)
    
    # 단어와 위치 추출
    positions = extract_text_with_position(image_path)
    print(f"추출된 단어들: {[pos[0] for pos in positions]}")
    
    # 다른 단어 찾기
    different_word, position = find_different_word_with_position(positions)
    if different_word:
        print(f"다른 단어: {different_word}")
        
        # 스크린샷 내 좌표를 실제 화면 좌표로 변환
        screen_x, screen_y = convert_image_coords_to_screen(position, screen_offset)
        
        # 변환된 좌표 출력
        print(f"변환된 좌표: {screen_x}, {screen_y}")
        
        # 실제 클릭 수행
        pyautogui.click(screen_x, screen_y)
    else:
        print("다른 단어를 찾을 수 없습니다.")

# 사용 예시
if __name__ == "__main__":
    # 화면에서 스크린샷을 찍을 영역의 좌표 (x_start, y_start, width, height)
    x_start = 952   # 스크린샷 영역의 시작 X 좌표
    y_start = 339   # 스크린샷 영역의 시작 Y 좌표
    width = 301     # 스크린샷의 너비 (1253 - 952)
    height = 346    # 스크린샷의 높이 (685 - 339)

    # 스크린샷 이미지 저장 경로
    image_path = "/Users/seonghyun/Desktop/quiz_images/quiz_screenshot.png"

    # 스크린샷을 찍은 영역의 시작 좌표 (해당 영역이 전체 화면 내에서의 시작점)
    screen_offset = (x_start, y_start)

    # 퀴즈 풀기 및 좌표 변환 후 클릭
    solve_quiz(x_start, y_start, width, height, image_path, screen_offset)