function [new_start, data_time, data_seg, time] = patterMatch(ev_value, rhythm_number)

    % Fit computation did not converge:
    % Fitting stopped because the number of iterations or function evaluations exceeded the specified maximum.
    
    % Fit found when optimization terminated:
    
    % General model Gauss4:
    %      f(x) = 
    %               a1*exp(-((x-b1)/c1)^2) + a2*exp(-((x-b2)/c2)^2) + 
    %               a3*exp(-((x-b3)/c3)^2) + a4*exp(-((x-b4)/c4)^2)
    % Coefficients (with 95% confidence bounds):
    %        a1 =       16.65  (9.804, 23.49)
    %        b1 =       172.1  (165.8, 178.4)
    %        c1 =       136.4  (121.6, 151.2)
    %        a2 =       11.89  (5.747, 18.04)
    %        b2 =       287.9  (189.8, 386)
    %        c2 =       248.7  (185.7, 311.6)
    %        a3 =       275.5  (-1356, 1907)
    %        b3 =        -148  (-1337, 1040)
    %        c3 =        1175  (-633.4, 2984)
    %        a4 =         272  (156.8, 387.3)
    %        b4 =        2233  (1865, 2600)
    %        c4 =        3177  (-2.571e+04, 3.207e+04)
    
    % Goodness of fit:
    %   SSE: 276.9
    %   R-square: 0.9999
    %   Adjusted R-square: 0.9999
    %   RMSE: 0.4313    
    
    

    time = 1/2302:1/2302:length(ev_value)/2302;

    a1 =       16.65;
    b1 =       172.1;
    c1 =        136.4;
    a2 =       11.89;
    b2 =       287.9;
    c2 =       248.7;
    a3 =       275.5;
    b3 =          -148;
    c3 =        1175;
    a4 =       272;
    b4 =        2233;
    c4 =        3177;

    x = 0:1500;
    L = a1*exp(-((x-b1)/c1).^2) + a2*exp(-((x-b2)/c2).^2) + a3*exp(-((x-b3)/c3).^2) + a4*exp(-((x-b4)/c4).^2);

    heng = []; zong = [];c = [];
    M1 = []; M2 = []; M2i = []; Mx = [];
    startpoint = []; heng2 = []; zong2 = [];
    startpoint2 =[]; data_seg = []; data_time = [];

    j=1;
    % 计算xcorr值
    for i= 1:100:length(ev_value)-1500
        heng(j,:) = i:i+1500;
        zong = ev_value(heng(j,:));
        c(j,:) = xcorr(L,zong,'normalized');
        j=j+1;
    end

    M1 = max(c,[],2);
    [M2,M2i] = sort(M1);
    Mx = M2i(length(M2)-rhythm_number*5:length(M2));

    % 取出比对那一段的开始点
    for ii = 1:length(Mx)
        startpoint(ii,:) = heng(Mx(ii),1);
    end
    startpoint = sort(startpoint);

    avg = [];start_point_avg = [];

    for jj = 1:length(startpoint)
        if isempty(avg) || abs(avg(end) - startpoint(jj)) < 500
            avg = [avg, startpoint(jj)];
        else
            start_point_avg = [start_point_avg, round(mean(avg))];
            avg = [];
            avg = [avg, startpoint(jj)];
        end
    end

    if ~isempty(avg)
        start_point_avg = [start_point_avg, round(mean(avg))];
    end

    % 根据起始点，找距离它前后的最大值点，作为真正segmentation的起始点，然后取值
    for iii = 1:length(start_point_avg)
        if start_point_avg(iii)-450 > 0
            heng2(iii,:) = start_point_avg(iii)-250:start_point_avg(iii)+50;
        else
            heng2(iii,:) = [ones(1,301 - (start_point_avg(iii)+50)),1:start_point_avg(iii)+50];
        end
        zong2(iii,:) = ev_value(heng2(iii,:));
    end
    [M3,M3i] = min(zong2,[],2);

    for j = 1:length(start_point_avg)
        startpoint2(:,j) = heng2(j,M3i(j));
    end

    startpoint2 = unique(startpoint2);
    avg = [];new_start = [];

    for jj = 1:length(startpoint2)
        if isempty(avg) || abs(avg(end) - startpoint2(jj)) < 500
            avg = [avg, startpoint2(jj)];
        else
            new_start = [new_start, round(mean(avg))];
            avg = [];
            avg = [avg, startpoint2(jj)];
        end
    end

    if ~isempty(avg)
        new_start = [new_start, round(mean(avg))];
    end

    for jj = 1:length(new_start)
        data_seg(jj,:) = ev_value(new_start(jj):new_start(jj)+1500);
        data_time(jj,:) = time(new_start(jj):new_start(jj)+1500);
    end