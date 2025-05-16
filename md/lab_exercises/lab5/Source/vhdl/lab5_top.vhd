library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity lab5_top is
    port (
        sysclk: in std_logic;
		btn: in std_logic_vector(3 downto 0);
        led4_r : out std_logic;
        led4_g : out std_logic;
        led4_b : out std_logic;
        led5_r : out std_logic;
        led5_g : out std_logic;
        led5_b : out std_logic
	);
end lab5_top;

architecture rtl of lab5_top is

    component clock_divider is
    generic ( OUTPUT_FREQUENCY : integer
    );
	port (
		clk_in: in std_logic;
		n_Reset: in std_logic;
		clk_out: out std_logic
     );
    end component clock_divider;
    
    component button_pulser is
    generic ( DELAY : integer;
              INTERVAL : integer
    );
    port (
        clk: in std_logic;
        btn: in std_logic;
        n_Reset: in std_logic;
        pulse: out std_logic
    );
    end component button_pulser;

    component pwm is
    generic ( PWM_RESOLUTION : integer
    );
    port (
        clk: in std_logic;
        n_Reset: in std_logic;
        pwm_ratio: in std_logic_vector(PWM_RESOLUTION - 1 downto 0);
        pwm_out: out std_logic
    );
    end component pwm;
    
    component channel_selector is
    port (
        clk: in std_logic;
        btn: in std_logic;
        n_Reset: in std_logic;
        next_channel: out std_logic_vector(1 downto 0)
    );
    end component channel_selector;
    
    component intensity is
    Generic (
        RGB_BITS: integer       
    );
    port ( clk: in std_logic;
           n_Reset: in std_logic;
           channel: in std_logic_vector(1 downto 0);
           increase: in std_logic;
           decrease: in std_logic;
           new_red: out std_logic_vector(RGB_BITS - 1 downto 0);
           new_green: out std_logic_vector(RGB_BITS - 1 downto 0);
           new_blue: out std_logic_vector(RGB_BITS - 1 downto 0)
    );
    end component intensity;
    
    -- general signals
    signal n_Reset: std_logic;
    signal div_clk: std_logic; -- divided clock signal from clock divider

    -- RGB channel selector
    signal channel: std_logic_vector(1 downto 0);
    signal channel_pulse: std_logic;
    signal rgb_led_5: std_logic_vector(0 to 2) := "001"; -- led indication which channel is selected

    -- color intensity
    signal intensity_pulse_btn: std_logic; -- state of buttons 2 and 3
    signal intensity_pulse: std_logic; -- pulse signal for intensity change
    signal intensity_r: std_logic_vector(7 downto 0);
    signal intensity_g: std_logic_vector(7 downto 0);
    signal intensity_b: std_logic_vector(7 downto 0);
    constant color_bits: integer := 8; -- set 8 to get 3 x 8 = 24 bits

 
begin
    
    n_Reset <= not btn(0);

    -- map signal "rgb_led_5" to actual output ports
    led5_r <= rgb_led_5(2);
    led5_g <= rgb_led_5(1);
    led5_b <= rgb_led_5(0);

    -- check the status of buttons 2 and 3 (decrease and increase color intensity);
    -- if both buttons are pressed, nothing happens            
    intensity_button_check: process(sysclk) is
    begin
        if rising_edge(sysclk) then
            if btn(2) = '1' and btn(3) = '1' then
                intensity_pulse_btn <= '0';
            elsif btn(2) = '1' or btn(3) = '1' then
                intensity_pulse_btn <= '1';
            else
                intensity_pulse_btn <= '0';
            end if;
        end if;
    end process intensity_button_check;
    
    -- indicate with RGB led 5 which channel on RGB led 4 is selected
    channel_indicator: process(channel) is
    begin
        if (channel = "00") then -- red
            rgb_led_5 <= "001";
        elsif (channel = "01") then -- green
            rgb_led_5 <= "010";
        elsif (channel = "10") then -- blue
            rgb_led_5 <= "100";
        else
            rgb_led_5 <= "000"; -- led off; something weird has happened
        end if;
    end process channel_indicator;            
    
    divider: clock_divider
    generic map (
        OUTPUT_FREQUENCY => 1e3
    )
    port map (
        clk_in => sysclk,
        n_Reset => n_Reset,
        clk_out => div_clk
    );
    
	channel_pulser: button_pulser
	generic map (
	   DELAY => 2000,
	   INTERVAL => 500
	)   
	port map (
	   clk => div_clk,
	   btn => btn(1),
	   pulse => channel_pulse,
	   n_Reset => n_Reset
	);
	
    intensity_pulser: button_pulser
	generic map (
	   DELAY => 1000,
	   INTERVAL => 50
	)   
	port map (
	   clk => div_clk,
	   btn => intensity_pulse_btn,
	   pulse => intensity_pulse,
	   n_Reset => n_Reset
	);
	
	pwm_r: pwm
	generic map (
	   PWM_RESOLUTION => color_bits
	)
	port map (
	   clk => sysclk,
	   n_Reset => n_Reset,
	   pwm_ratio => intensity_r,
	   pwm_out => led4_r
	);

	pwm_g: pwm
	generic map (
	   PWM_RESOLUTION => color_bits
	)
	port map (
	   clk => sysclk,
	   n_Reset => n_Reset,
	   pwm_ratio => intensity_g,
	   pwm_out => led4_g
	);

	pwm_b: pwm
	generic map (
	   PWM_RESOLUTION => color_bits
	)
	port map (
	   clk => sysclk,
	   n_Reset => n_Reset,
	   pwm_ratio => intensity_b,
	   pwm_out => led4_b
	);
	
    rgb_channel_selector: channel_selector
    port map (
        clk => channel_pulse,
        btn => btn(1),
        n_Reset => n_Reset,
        next_channel => channel
    );
	
	intensity_selector: intensity
	generic map (
	   RGB_BITS => color_bits
	)
	port map (
	   clk => intensity_pulse,
	   n_Reset => n_Reset,
	   channel => channel,
	   increase => btn(3),
	   decrease => btn(2),
	   new_red => intensity_r,
	   new_green => intensity_g,
	   new_blue => intensity_b
    );	   
	
end rtl;
